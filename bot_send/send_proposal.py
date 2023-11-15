from loguru import logger
from aiogram import Dispatcher
from data.config import admins
from aiogram.types import InputFile


async def send_proposal(dp: Dispatcher, file, fio, variant_proposal):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=f'{fio} отправил вариант заявки "{variant_proposal}"')
            with open(file, 'rb') as document:
                await dp.bot.send_document(chat_id=admin, document=InputFile(document))
        except Exception as err:
            logger.exception(err)
