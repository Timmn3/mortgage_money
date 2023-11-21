from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsSubscriber
from keyboards.inline import ikb_menu
from loader import dp


# Если команда menu, то выводи инлайн клавиатуру
@dp.message_handler(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Выберете один из пунктов меню:', reply_markup=ikb_menu)



