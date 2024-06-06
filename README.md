# 2-factor authentification using face recognition

Чёрт побери да это настоящий феррари среди ржавых жигулей. Общение 2 модулей построено чисто на POST запросах, причём их вариативность поражает. Наконец-то мы применяем навыки, полученные ранее и делаем это с удовольствием.

Систему отвечающую за вход начал писать N, дописывали мы вместе прямыми руками, растущими из правильного места.

Приложение-болванку писал L, поэтому она вся на костылях, но работает чётко (после фиксов), так что грех жаловаться. 

# Примеры работы main

Вход:

![image](https://github.com/Blaffy9090/face_hackatonishe/assets/119712032/0f0a5c67-9c9c-46b3-8bb4-cfdce31b6de8)

Интерфейс(тема зависит от системной темы):

![image](https://github.com/Blaffy9090/face_hackatonishe/assets/119712032/e176611a-5205-42ca-b39f-138eab61917a)

Редактор профиля:

![image](https://github.com/Blaffy9090/face_hackatonishe/assets/119712032/07cbf7aa-46ff-4031-afe6-f9e81b1a20a4)


# Пример кода, отправляемого на почту при неудачном входе с камеры:

![image](https://github.com/Blaffy9090/face_hackatonishe/assets/119712032/a1bb2d39-4a23-444c-8a5e-5e91bbd5130d)

# Пример запроса, передаваемого в handler библиотеки

 tmp = {
     "auth":None,
     "type":"registration",
     "data":{
         "email": "user1@example.com",
         "password": "securePassword123",
         "name": "John Doe"
     }
 }   

 tmp = {
     "auth":True,
     "type":"edit",
     "data":{
         "email": "user1@example.com",
         "password": "securePassword123",
         "name": "John Doe",
         "photo": "C:\Users\AEZAKMI\Downloads\Test.png"
     }
 }
