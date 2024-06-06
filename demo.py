import json
import os
import sys
import cv2
import face_recognition
import hashlib
import shutil
import datetime
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


folder_name = "UsersDB"
image_path = "Users_photo"
file_name = "Users.json"
file_path = folder_name + "/" + file_name

fromaddr = "pabl0bs@mail.ru"
password = "00NzbZKWLqKWabwzeDrJ"

def hash_password(password):
    salt = "sometext"
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed_password


def raise_error(message):
    error = {
        "state": "error",
        "text": message
    }
    return error


def raise_success(tip, message):
    return {
        "state": tip,
        "text": message
    }


def raise_success_name(tip, message, name):
    return {
        "state": tip,
        "text": message,
        "name": name
    }


def raise_success_trio(tip, message, name, faceid):
    return {
        "state": tip,
        "text": message,
        "name": name,
        "faceid":faceid
    }


def check_state():
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            buff = []
            json.dump(buff, file)


def find_user(pathfile, email):
    with open(pathfile, 'r', encoding='utf-8') as file:
        dic = json.load(file)
        for user in dic:
            if user['email'] == email:
                return user
        return None


def registration(post):
    check_state()

    if find_user(file_path, post['email']):
        return raise_error("User already exists")

    post["password"] = hash_password(post["password"])
    post["faceid"] = False

    buff = []
    with open(file_path, 'r', encoding='utf-8') as file:
        buff = json.load(file)
        buff.append(post)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buff, file)

    return raise_success("unlogin", "Registered successfully")


def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def sendcode(mail, code):
    toaddr = mail

    # Создаем письмо
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Код подтверждения"

    txt = MIMEText(
        "Никому не сообщайте код: " + code + "\n" + "Если вы не запрашивали код, то проигнорируйте это письмо", 'plain',
        'utf-8')

    msg.attach(txt)
    # Подключаемся к серверу и отправляем письмо
    server = smtplib.SMTP('smtp.mail.ru', 2525)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def gencode(mail):
    code = str(generateOTP())
    time = datetime.datetime.now().timestamp()

    sendcode(mail, code)
    #print(mail, code)
    code = hash_password(code)
    slov = {}
    slov['code'] = code
    slov['time'] = time

    #print(slov)
    with open('UsersDB/code.json', 'w', encoding='utf-8') as file:
        json.dump(slov, file)


def login(post):
    check_state()
    user_data = find_user(file_path, post['email'])
    if not user_data:
        return raise_error("This user does not exist")

    post["password"] = hash_password(post["password"])
    if user_data["password"] == post["password"]:
        if 'code' in post:
            with open('UsersDB/code.json', 'r', encoding='utf-8') as file:
                buff = json.load(file)
            try:
                os.remove('UsersDB/code.json')
            except FileNotFoundError:
                pass
            if not((datetime.datetime.now().timestamp() <= buff["time"] + 300) and (datetime.datetime.now().timestamp() >= buff["time"])):
                return raise_error("Expired code")
            if (hash_password(post["code"]) == buff["code"]):
                return raise_success_trio("login", "Logged successfully", user_data["name"],user_data["faceid"])
            else:
                return raise_error("Wronk code")

        if (user_data["faceid"]):
            way1 = image_path + "/" + "buff" + ".jpg"
            way2 = image_path + "/" + post["email"] + ".jpg"
            take_picture(way1)
            flag = analyze_photo(way1, way2)
            try:
                os.remove(way1)
            except FileNotFoundError:
                pass

            if flag == 1:
                gencode(post['email'])
                return raise_error("Can't find face in image")
            if flag == 2:
                return raise_error("This face is not recognized")
            if flag == 3:
                return raise_success_trio("login", "Logged successfully", user_data["name"], user_data["faceid"])
        else:
            return raise_success_name("login", "Logged successfully", user_data["name"])
    else:
        return raise_error("Wrong password")


def rename_file_in_directory(old_name, new_name):
    directory = os.path.join(image_path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == old_name:
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                #print(f"Файл {old_path} был переименован в {new_path}")


def edit_user(post):
    if 'oldemail' in post:
        user_data = find_user(file_path, post['oldemail'])
        try:
            rename_file_in_directory((post["oldemail"]+".jpg"), (post["email"]+".jpg"))
        except FileNotFoundError:
            pass
        del post['oldemail']
    else:
        user_data = find_user(file_path, post['email'])

    post["faceid"] = user_data["faceid"]

    #(post)

    if ("photo" in post):
        old = post["photo"]
        test = old.split(".")[-1]
        if test != "jpg":
            return raise_error("Wrong file type!")
        new = image_path + "/" + post["email"] + ".jpg"
        if check_photo_face(old) and check_file_size(old):
            #print("old photo good")
            shutil.copyfile(old, new)
            post["faceid"] = True
            del post['photo']
        else:
            #print("old photo bad")
            return raise_error("Face not recognized")

    post["password"] = hash_password(post["password"])
    buff = []
    with open(file_path, 'r', encoding='utf-8') as file:
        buff = json.load(file)
        buff.remove(user_data)
        buff.append(post)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buff, file)

    return raise_success_trio("login", "Logged successfully", post["name"], post["faceid"])

def delete_user(post):
    user_data = find_user(file_path, post['email'])

    with open(file_path, 'r', encoding='utf-8') as file:
        buff = json.load(file)
        buff.remove(user_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(buff, file)

    return raise_success("unlogin", "Deleted successfully")

def take_picture(name_file="im1.jpg"):
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    while True:
        ret, frame = cap.read()
        # overlay = frame.copy()
        # cv2.rectangle(overlay, (250, 160), (380, 350), (128, 128, 128), 2)
        # cv2.putText(overlay, "Put your face into frame", (220, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        # # Показываем кадр в окне
        # alpha = 0.7
        # cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.imshow('Video', frame)

        # Ожидаем нажатия клавиши "Space" для съемки фотографии
        if cv2.waitKey(1) & 0xFF == ord(' '):
            #frame = frame[230:400, 150:360]
            cv2.imwrite(name_file, frame)
            cap.release()
            cv2.destroyAllWindows()
            break
    #print("Лицо отсканировано")


def check_file_size(file_location, max_size_in_bytes=20000000):
    file_size = os.path.getsize(file_location)
    if file_size <= max_size_in_bytes:
        return True
    else:
        return False


def check_photo_face(file_location):
    try:
        f = face_recognition.load_image_file(file_location)
        f = cv2.cvtColor(f, cv2.COLOR_BGRA2BGR)
        f2 = face_recognition.face_locations(f)[0]
        if len(face_recognition.face_locations(f)) != 1:
            return False
        f2 = face_recognition.face_encodings(f)[0]
        return True
    except IndexError as er:
        return False


def analyze_photo(path_file1, path_file2):
    #print("Анализируем лицо...")

    if not check_file_size(path_file1):
        raise_error("Foto has very big size!")

    try:
        first = face_recognition.load_image_file(path_file1)
        first = cv2.cvtColor(first, cv2.COLOR_BGRA2BGR)
        first_face = face_recognition.face_locations(first)[0]
        if len(face_recognition.face_locations(first)) != 1:
            return 1
        encode_first = face_recognition.face_encodings(first)[0]
    except IndexError as er:
        return 1

    basing = face_recognition.load_image_file(path_file1)
    basing = cv2.cvtColor(basing, cv2.COLOR_BGRA2BGR)

    user_face = face_recognition.face_locations(basing)[0]
    encodenyface = face_recognition.face_encodings(basing)[0]
    cv2.rectangle(first, (first_face[3], first_face[0]), (first_face[1], first_face[2]), (255, 0, 255), 2)

    # cv2.imshow("test", first)
    # cv2.waitKey(0)
    try:
        second = face_recognition.load_image_file(path_file2)
        second = cv2.cvtColor(second, cv2.COLOR_BGRA2BGR)
        second_face = face_recognition.face_locations(second)[0]
        encode_second = face_recognition.face_encodings(second)[0]
    except IndexError as er:
        return 1

    result = face_recognition.compare_faces([encodenyface], encode_second)
    resulting = str(result)

    if resulting == "[True]":
        return 3
    else:
        return 2


def handler(post):
    for key in post:
        if key == None:
            return raise_error('None in POST error')
        if post[key] == None:
            return raise_error('None in POST error')

    for key in post["data"]:
        if key == None:
            return raise_error('None in POST error')
        if post["data"][key] == None:
            return raise_error('None in POST error')


    if (post['auth'] == False):
        match post['state']:
            case 'registration':
                return registration(post['data'])
            case 'login':
                return login(post['data'])
            case _:
                return raise_error('Unexpected error')
    elif (post['auth'] == True):
        match post['state']:
            case 'edit':
                return edit_user(post['data'])
            case 'delete':
                return delete_user(post['data'])
            case _:
                return raise_error('Unexpected error')
    else:
        return raise_error('Unexpected error')

if __name__ == "__main__":
    print("Hi")
    # tmp = {
    #     "auth":None,
    #     "type":"registration",
    #     "data":{
    #         "email": "user1@example.com",
    #         "password": "securePassword123",
    #         "name": "John Doe"
    #     }
    # }
    # print(handler(tmp))
    #
    # tmp = {
    #     "auth":True,
    #     "type":"edit",
    #     "data":{
    #         "email": "user1@example.com",
    #         "password": "securePassword123",
    #         "name": "John Doe",
    #         "photo": "C:\Users\Hovro\Downloads\Test.png"
    #     }
    # }
    # print(handler(tmp))
    #
    # data = {
    #     "email": "user1@example.com",
    #     "password": "securePassword123",
    #     "photo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/4QAYRXhpZgAATU0AKgAAAAgAAwEsAAUAAAABAAAA...",
    #     "name": "John Doe"
    # }
    # print(handler(tmp))

    #print(find_user("UsersDB/Users2.json", "user5@example.com"))

    # take_picture()
    # analyze_user()
