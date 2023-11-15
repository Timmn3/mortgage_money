from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from loader import dp
from utils.db_api import users_commands as commands


@dp.message_handler(Command('balance'))  # по каманде /balance выводит баланс
async def show_balance(message: types.Message):
    pass
    # balance = await commands.user_balance(int(message.from_user.id))
    # await message.answer(f'Ваш баланс: {balance} ₽', reply_markup=ikb_balance)
