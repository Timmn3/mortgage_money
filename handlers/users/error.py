from aiogram import types
from loader import dp

@dp.message_handler()
async def command_error(message: types.Message):
    pass
    # await message.answer(f'Команда {message.text} не найдена')
