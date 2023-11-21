""" Проходит по всем user_id и обновляет список количества рефералов"""

from filters import AdminsMessage
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command

from utils.db_api.users_commands import reset_all_user_data, get_all_user_ids, save_count_levels, \
    find_user_by_who_invited


# команда /message отправить сообщения всем пользователям
@dp.message_handler(AdminsMessage(), Command('update_referrals'))
async def send_message(message: types.Message):
    await message.answer('Подождите...')
    await update_referrals()
    await message.answer('Данные по рефералам обновлены')


async def update_referrals():
    # обнуляем всем пользователям значения level и bonus_1
    await reset_all_user_data()

    # получаем список всех user_id
    user_ids = await get_all_user_ids()

    for user in user_ids:
        user_id_1 = await find_user_by_who_invited(str(user))
        user_id_2 = await find_user_by_who_invited(str(user_id_1))
        user_id_3 = await find_user_by_who_invited(str(user_id_2))
        user_id_4 = await find_user_by_who_invited(str(user_id_3))
        user_id_5 = await find_user_by_who_invited(str(user_id_4))

        if user_id_1 != '0' and user_id_1 is not None:
            await save_count_levels(user, 1)
        if user_id_2 != '0' and user_id_2 is not None:
            await save_count_levels(user, 2)
        if user_id_3 != '0' and user_id_3 is not None:
            await save_count_levels(user, 3)
        if user_id_4 != '0' and user_id_4 is not None:
            await save_count_levels(user, 4)
        if user_id_5 != '0' and user_id_5 is not None:
            await save_count_levels(user, 5)


