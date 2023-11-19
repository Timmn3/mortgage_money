from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.inline.rules_and_contracts import ikb_rules_contracts
from loader import dp


# Если команда menu, то выводи инлайн клавиатуру
@dp.message_handler(Command('rules_contracts'))
async def menu(message: types.Message):
    await message.answer('Ознакомьтесь с документами:', reply_markup=ikb_rules_contracts)



