from aiogram import Dispatcher
from loader import scheduler
from loguru import logger
from asyncio import sleep
from utils.db_api.admin_commands import get_newsletter_text, get_newsletter_period
from utils.db_api.users_commands import get_all_user_ids
from loader import dp
from apscheduler.triggers.interval import IntervalTrigger


async def send_message_to(dpr: Dispatcher):
    text = await get_newsletter_text()
    # если текст не пустой
    if text:
        users_id = await get_all_user_ids()
        for user in users_id:
            try:
                await dpr.bot.send_message(chat_id=user, text=text)
                await sleep(0.25)  # 4 сообщения в секунду
            except Exception as e:
                logger.error(e)


# отправка по времени
async def schedule_jobs():
    day = await get_newsletter_period()
    trigger = IntervalTrigger(days=day, hours=12, minutes=0)  # Укажите интервал в часах
    scheduler.add_job(send_message_to, trigger, args=(dp,))
