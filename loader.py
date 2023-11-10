import tzlocal
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from utils.db_api.db_gino import db

# создаем переменную бота с токеном нашего бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

# создаем диспетчер
dp = Dispatcher(bot, storage=storage)

# инициализируем scheduler
scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

__all__ = ['bot', 'storage', 'dp', 'db', 'scheduler']
