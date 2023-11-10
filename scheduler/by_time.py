from aiogram import Dispatcher

from data import config
from handlers.users.balance import send_message_users_balance_lower_100

from loader import scheduler
# для парсигна последней страницы
from parser.parse_page import add_in_bd_page
import requests


async def send_message_to(dpr: Dispatcher):
    await dpr.bot.send_message(config.admins[0], 'Сообщение по таймеру')


# запрос на страницу
def request_page():
    url = 'https://www.google.com/'
    requests.get(url)


# https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28

def schedule_send():
    scheduler.add_job(request_page, 'interval', minutes=1)


# парсинг по времени
async def schedule_jobs():
    # scheduler.add_job(send_message_to, 'interval', seconds=2, args=(dp,))  # отправка каждые 5 сек
    # scheduler.add_job(send_message_to, "date", run_date=datetime(2022, 10, 19, 19, 57), args=(dp,)) #отправка по дате
    # scheduler.add_job(add_in_bd_page, 'cron', hour=20, minute=25, end_date='2025-05-30',
    #                   args=(parse_page()))  # отправка по врем

    try:
        scheduler.add_job(add_in_bd_page, 'cron', hour=10, minute=10, end_date='2025-05-30')
        scheduler.add_job(add_in_bd_page, 'cron', hour=13, minute=10, end_date='2025-05-30')
        scheduler.add_job(add_in_bd_page, 'cron', hour=16, minute=10, end_date='2025-05-30')
        scheduler.add_job(add_in_bd_page, 'cron', hour=18, minute=10, end_date='2025-05-30')
        scheduler.add_job(add_in_bd_page, 'cron', hour=22, minute=10, end_date='2025-05-30')
    except Exception:
        print('Ошибка парсинга по времени')


# отправка сообщения о балансе ниже 100 р
def schedule_balance():
    try:
        scheduler.add_job(send_message_users_balance_lower_100, 'cron', hour=12, minute=0, end_date='2025-05-30')
        scheduler.add_job(send_message_users_balance_lower_100, 'cron', hour=19, minute=0, end_date='2025-05-30')
    except Exception:
        print('Ошибка отправки сообщения о балансе')
