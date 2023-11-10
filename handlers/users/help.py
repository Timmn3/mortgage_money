from aiogram import types

from data.config import help_user
from loader import dp

@dp.message_handler(text="/help")
async def command_help(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! \n'
                         f'Тебе нужна помощь? Напиши в техподдержку {help_user}')
