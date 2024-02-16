from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher.filters.state import StatesGroup, State
from filters import IsSubscriber
from handlers.admin.update_referrals import find_keys_by_value, calculate_levels
from keyboards.cancel import keyboard_cancel
from loader import dp
from utils.db_api.users_commands import get_user_referrals, print_user_levels, reset_user_data_by_id, save_count_levels, \
    get_user_id_who_invited_dict
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


@dp.message_handler(text="/ref")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    try:
        ref_link = await get_start_link(payload=message.from_user.id)
        await reset_user_data_by_id(message.from_user.id)
        dict_user = await get_user_id_who_invited_dict(message.from_user.id)
        await calculate_levels(dict_user, message.from_user.id)
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
    except Exception as e:
        pass


class Ref(StatesGroup):
    id = State()  # вариант заявки


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
        try:
            user = int(message.text)
            ref = await print_user_levels(user)

            await message.answer(f'У тебя {ref[1]} пользователей в команде\n'
                                 f'{ref[0]}\n')
        except Exception:
            await message.answer('Пользователь не найден')
        await state.finish()
