import tkinter
from tkinter import filedialog
from tkinter import messagebox

import customtkinter
from PIL import Image, ImageTk

from demo import handler

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

n = ''
p = ''
m = ''
f = ''
d = ''
cde = ''
one_time_code = ''


def handler_log_ps(eml, ps, cd):
    data = {
        "auth": False,
        "state": "login",
        "data": {
            "email": eml,
            "password": ps,
            "code": cd
        }
    }
    return handler(data)


def handler_log(eml, ps):
    data = {
        "auth": False,
        "state": "login",
        "data": {
            "email": eml,
            "password": ps
        }
    }
    return handler(data)


def handler_reg(eml, ps, nam):
    data = {
        "auth": False,
        "state": "registration",
        "data": {
            "email": eml,
            "password": ps,
            "name": nam
        }
    }
    return handler(data)


def handler_del(eml):
    data = {
        "auth": True,
        "state": "delete",
        "data": {
            "email": eml
        }
    }
    return handler(data)


def button_function():
    global home_app, n, m, p, a
    print(n)
    app.destroy()
    home_app = customtkinter.CTk()
    home_app.geometry("1280x720")
    home_app.title('Welcome')

    frame = customtkinter.CTkFrame(master=home_app, width=600, height=600, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    l1 = customtkinter.CTkLabel(master=frame, text="Hello, " + n, font=('Century Gothic', (10000 / len(n)) ** 0.5))
    l1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

    def update_color(index=0):
        colors = ["#FF0000", "#FF1900", "#FF3300", "#FF4C00", "#FF6600",
                  "#FF7F00", "#FF9900", "#FFB200", "#FFCC00", "#FFE500",
                  "#FFFF00", "#E5FF00", "#CCFF00", "#B2FF00", "#99FF00",
                  "#7FFF00", "#66FF00", "#4CFF00", "#33FF00", "#19FF00",
                  "#00FF00", "#00FF19", "#00FF33", "#00FF4C", "#00FF66",
                  "#00FF7F", "#00FF99", "#00FFB2", "#00FFCC", "#00FFE5",
                  "#00FFFF", "#00E5FF", "#00CCFF", "#00B2FF", "#0099FF",
                  "#007FFF", "#0066FF", "#004CFF", "#0033FF", "#0019FF",
                  "#0000FF", "#1900FF", "#3300FF", "#4C00FF", "#6600FF",
                  "#7F00FF", "#9900FF", "#B200FF", "#CC00FF", "#E500FF",
                  "#FF00FF", "#FF00E5", "#FF00CC", "#FF00B2", "#FF0099",
                  "#FF007F", "#FF0066", "#FF004C", "#FF0033", "#FF0019"]
        l1.configure(text_color=colors[index])
        frame.after(650, update_color, (index + 1) % len(colors))

    update_color()

    edit_profile_button = customtkinter.CTkButton(master=frame, text="Edit Profile", command=edit_profile_function,
                                                  corner_radius=15)
    edit_profile_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    log_out_button = customtkinter.CTkButton(master=frame, text="Log Out", command=log_out_function, corner_radius=15)
    log_out_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    home_app.mainloop()


def log_out_function():
    global home_app, n
    home_app.destroy()
    login_screen()


def register_user():
    reg_app.withdraw()
    app.deiconify()


def reg_function():
    global reg_app

    app.withdraw()
    reg_app = customtkinter.CTk()
    reg_app.geometry("600x440")
    reg_app.title('Register')

    frame = customtkinter.CTkFrame(master=reg_app, width=320, height=400, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Register", font=('Century Gothic', 20))
    l2.place(x=50, y=25)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=75)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    entry2.place(x=50, y=125)

    entry3 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry3.place(x=50, y=175)

    def submit_registration():
        username = entry1.get()
        email = entry2.get()
        password = entry3.get()
        a = handler_reg(email, password, username)
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields must be filled")
        if not (a["state"] == "error"):
            messagebox.showinfo("Success", a["text"])
            register_user()
        if a["state"] == "error":
            messagebox.showerror("Error", a["text"])

    button1 = customtkinter.CTkButton(master=frame, width=220, text="Register", command=submit_registration,
                                      corner_radius=6)
    button1.place(x=50, y=225)

    button_back = customtkinter.CTkButton(master=frame, width=220, text="Back to Login",
                                          command=lambda: switch_to_login(reg_app), corner_radius=6)
    button_back.place(x=50, y=275)

    reg_app.mainloop()


def switch_to_login(current_app):
    current_app.withdraw()
    app.deiconify()


def imge():
    global d
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    d = file_path
    return d


def edit_profile_function():
    global edit_app, d, f, m, p, n, a

    home_app.withdraw()
    edit_app = customtkinter.CTk()
    edit_app.geometry("600x440")
    edit_app.title('Edit Profile')

    frame = customtkinter.CTkFrame(master=edit_app, width=320, height=450, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Edit Profile", font=('Century Gothic', 20))
    l2.place(x=50, y=25)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=75)
    entry1.insert(0, n)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    entry2.place(x=50, y=125)
    entry2.insert(0, m)

    entry3 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry3.place(x=50, y=175)
    entry3.insert(0, p)

    def submit_edit():
        global f, n, a
        oldem = m
        username = entry1.get()
        email = entry2.get()
        password = entry3.get()

        data = {
            "auth": True,
            "state": "edit",
            "data": {
                "email": email,
                "password": password,
                "name": username,
            }
        }
        if not (oldem == email):
            data['data']["oldemail"] = oldem
        if not (d == ''):
            data['data']["photo"] = d
        if not (d == ''):
            data['data']["faceid"] = True
        if d == '':
            data['data']["faceid"] = False
        print(data)
        a = handler(data)

        if not username or not email or not password:
            messagebox.showerror("Error", "All fields must be filled")
        if (a["state"] == "error"):
            messagebox.showerror("Error", a["text"])
        else:
            n = username
            switch_to_home(edit_app)

    button1 = customtkinter.CTkButton(master=frame, width=220, text="Save Changes", command=submit_edit,
                                      corner_radius=6)
    button1.place(x=50, y=225)

    button_back = customtkinter.CTkButton(master=frame, width=220, text="Back to Home",
                                          command=lambda: switch_to_home(edit_app), corner_radius=6)
    button_back.place(x=50, y=275)

    switch_var = tkinter.StringVar(value="System")

    add_face_button = customtkinter.CTkButton(master=frame, text="Add Face", command=imge, corner_radius=6)
    add_face_button.place(x=50, y=325)
    add_face_button.place_forget()

    def killer1(eml):
        global edit_app
        handler_del(eml)
        edit_app.destroy()
        log_out_function()

    button_back = customtkinter.CTkButton(master=frame, width=220, text="Delete",
                                          command=lambda: killer1(m), corner_radius=6, fg_color="red",
                                          hover_color="#ff4c4c")
    button_back.place(x=50, y=375)

    def switch_theme():
        global n
        theme = switch_var.get()
        customtkinter.set_appearance_mode(theme)
        if theme == "Dark":
            add_face_button.place(x=50, y=325)
        else:
            add_face_button.place_forget()

    theme_switcher = customtkinter.CTkSwitch(master=frame, text="Face ID", variable=switch_var, onvalue="Dark",
                                             offvalue="Black", command=switch_theme)
    theme_switcher.place(x=200, y=327)

    edit_app.mainloop()


def switch_to_home(current_app):
    global n
    current_app.withdraw()
    home_app.deiconify()


def login_screen():
    global app, img1, img2, img3, n, p, m

    app = customtkinter.CTk()
    app.geometry("600x440")
    app.title('Login')

    img1 = ImageTk.PhotoImage(Image.open("./assets/pattern.png"))
    img2 = ImageTk.PhotoImage(Image.open("assets/google.png").resize((20, 20), Image.LANCZOS))
    img3 = ImageTk.PhotoImage(Image.open("assets/vk.png").resize((20, 20), Image.LANCZOS))

    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=320, height=420, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
    l2.place(x=50, y=45)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    entry1.place(x=50, y=110)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=165)

    def submit_login():
        global n, f, p, m, subm_log_app, cde
        email = entry1.get()
        password = entry2.get()

        p = password
        m = email

        a = handler_log(email, password)
        if not email or not password:
            messagebox.showerror("Error", "All fields must be filled")
        if not (a["state"] == 'error'):
            n = a["name"]
            p = password
            m = email
            messagebox.showinfo("Success", a["text"])
            button_function()
        if a["state"] == 'error':
            if a['text'] == "Can't find face in image":
                subm_log_app = customtkinter.CTk()
                subm_log_app.geometry("600x440")
                subm_log_app.title('Fix')

                frame = customtkinter.CTkFrame(master=subm_log_app, width=600, height=600, corner_radius=15)
                frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                label = customtkinter.CTkLabel(master=frame,
                                               text="Do you want to get a one-time code to log in to your account?(You will have 5 minutes to enter it)")

                label.pack(pady=20)

                def open_code_window():
                    global cde, p, m, n, subm_log_app
                    code_window = customtkinter.CTk()
                    code_window.geometry("400x200")
                    code_window.title('Enter Code')

                    frame_code = customtkinter.CTkFrame(master=code_window, width=300, height=150, corner_radius=15)
                    frame_code.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                    label_code = customtkinter.CTkLabel(master=frame_code, text="Enter one-time code:")
                    label_code.pack(pady=10)

                    entry_code = customtkinter.CTkEntry(master=frame_code, width=220)
                    entry_code.pack(pady=5)

                    def handle_code(code):
                        global cde, p, m, a, n, f, subm_log_app
                        cde = code
                        print(m, p, cde)
                        a = handler_log_ps(m, p, cde)
                        print(a)
                        if a["state"] == "login":
                            n = a["name"]
                            f = a["faceid"]
                            messagebox.showinfo("Sucess", a["text"])
                            code_window.destroy()
                            subm_log_app.destroy()
                            button_function()
                        elif a["state"] == "error":
                            messagebox.showerror("Error", a["text"])
                            code_window.destroy()
                            subm_log_app.destroy()
                        else:
                            messagebox.showerror("Error", "Unexpected Error")
                            code_window.destroy()
                            subm_log_app.destroy()

                    submit_button = customtkinter.CTkButton(master=frame_code, text="Submit",
                                                            command=lambda: handle_code(entry_code.get()))
                    submit_button.pack(pady=10)

                    code_window.mainloop()

                button1 = customtkinter.CTkButton(master=frame, text="Yes", command=open_code_window)
                button1.pack(pady=10)

                button2 = customtkinter.CTkButton(master=frame, text="Cancel", command=subm_log_app.destroy)
                button2.pack(pady=10)

                subm_log_app.mainloop()
            else:
                messagebox.showerror("Error", a["text"])
                # ТУПО ВЫВЕСТИ ТЕКСТ ОШИБКИ (СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЯ(НЕ ЗАЛОГИН7ЕН) НЕ МЕНЯТЬ)

    def killer():
        app.destroy()

    button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=submit_login, corner_radius=6)
    button1.place(x=50, y=225)

    button2 = customtkinter.CTkButton(master=frame, width=220, text="Register", command=reg_function, corner_radius=6)
    button2.place(x=50, y=260)

    button_google = customtkinter.CTkButton(master=frame, image=img2, text="Google", width=100, height=20,
                                            compound="left", fg_color='white', text_color='black',
                                            hover_color='#AFAFAF')
    button_google.place(x=50, y=300)

    button_vk = customtkinter.CTkButton(master=frame, image=img3, text="VK", width=100, height=20, compound="left",
                                        fg_color='white', text_color='black', hover_color='#AFAFAF')
    button_vk.place(x=170, y=300)

    button4 = customtkinter.CTkButton(master=frame, width=220, text="Exit", command=killer, corner_radius=6,
                                      fg_color="red", hover_color="#ff4c4c")
    button4.place(x=50, y=360)

    app.mainloop()


login_screen()
