import os
from dotenv import load_dotenv


load_dotenv('config.env')


user_token = os.getenv('user_token')
comm_token = os.getenv('comm_token')
DSN = os.getenv('DSN')


if user_token is None or comm_token is None or DSN is None:
    print("Ошибка чтения токенов из файла config.env")
else:
    print("Токены успешно прочитаны:")


