from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from loader import dp
from utils.db_api.users_commands import get_user_referrals


@dp.message_handler(text="/ref")  # создаем хэндлер
async def command_ref(message: types.Message):  # создаем асинхронную функцию
    ref_link = await get_start_link(payload=message.from_user.id)
    count_refs = await get_user_referrals(message.from_user.id)
    count = 0
    if count_refs:
        count_dict = count_refs.split(',')
        count = len(count_dict)
    else:
        count = 0
    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'У тебя {count} реферала(ов)\n'
                         f'Ваша реферальная ссылка:\n'
                         f'{ref_link}')
