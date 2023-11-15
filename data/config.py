import os

from dotenv import load_dotenv

# запускаем функцию, которая загружает переменное окружение из файла .env
load_dotenv()

# Токен бота
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

# список администраторов бота
admins = [1089138631]

# user для обращения пользователей
help_user = '@Stoloto_support'

ip = os.getenv('IP')
PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{ip}/{DATABASE}'
