from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from filters import IsSubscriber
from keyboards.cancel import keyboard_cancel
from loader import dp
from utils.db_api.users_commands import get_user_referrals, print_user_levels, delete_user
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class Del(StatesGroup):
    id = State()  # вариант заявки


@dp.message_handler(text="/delete_user")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    await message.answer(f'Введи id', reply_markup=keyboard_cancel)
    await Del.id.set()


@dp.message_handler(state=Del.id)
async def delete_user_id(message: types.Message, state: FSMContext):
    text = message.text
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        try:
            user = int(message.text)
            await delete_user(user)
            await message.answer('Пользователь удален!')
        except Exception:
            await message.answer('Пользователь не найден')
        await state.finish()

