from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher.filters.state import StatesGroup, State
from filters import IsSubscriber
from loader import dp
from utils.db_api.users_commands import get_user_referrals, print_user_levels
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

@dp.message_handler(text="/ref")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    ref_link = await get_start_link(payload=message.from_user.id)
    ref = await print_user_levels(message.from_user.id)

    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'У тебя {ref[1]} пользователей в команде\n'
                         f'{ref[0]}\n'
                         f'Ваша реферальная ссылка:\n'
                         f'{ref_link}\n'
                         f'🟢Для реферальной регистрации Ваш адресат должен 👉ОБЯЗАТЕЛЬНО перейти, КЛИКНУВ по ссылке '
                         f'в телеграмм, которую вы ему отправили.\n'
                         f'💢НЕ вставлять в поиск\n'
                         f'💢НЕ вставлять в браузер\n'
                         f'💢НЕ вставлять в WhatsApp')


class Ref(StatesGroup):
    id = State()  # вариант заявки

keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(KeyboardButton('Отмена'))


@dp.message_handler(text="/ref_id")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    await message.answer(f'Введи id', reply_markup=keyboard_cancel)
    await Ref.id.set()


@dp.message_handler(state=Ref.id)
async def process_fio(message: types.Message, state: FSMContext):
    text = message.text
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        user = int(message.text)
        ref = await print_user_levels(user)

        await message.answer(f'У тебя {ref[1]} пользователей в команде\n'
                             f'{ref[0]}\n')
        await state.finish()
