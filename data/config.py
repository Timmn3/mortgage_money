import os

from dotenv import load_dotenv

# запускаем функцию, которая загружает переменное окружение из файла .env
load_dotenv()

# Токен бота
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

# список администраторов бота
admins = [1089138631, 6075652143]
chat_ids = [-1001878077008]
# user для обращения пользователей
help_user = '@WinnRusso'

ip = os.getenv('IP')
PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{ip}/{DATABASE}'
