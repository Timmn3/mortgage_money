from aiogram.utils.deep_linking import get_start_link

from filters.subscription import subscriber
from loader import dp
from aiogram import types
from utils.db_api.users_commands import get_user_referrals, get_user_balance, get_usernames, get_bonus_1_value, \
    find_user_ids_by_nik


@dp.callback_query_handler(text='Личный кабинет')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        ref_link = await get_start_link(payload=call.from_user.id)
        referral_usernames = await find_user_ids_by_nik(str(call.from_user.id))
        if not referral_usernames:
            result_string = 'у Вас нет рефералов'
        else:
            formatted_usernames = [f'@{username}' for username in referral_usernames]

            # Join the formatted usernames into a comma-separated string
            result_string = ', '.join(formatted_usernames)

        bonus_1 = await get_bonus_1_value(call.from_user.id)
        await call.message.answer(f'Твоя реферальная ссылка: \n{ref_link} \n'
                                  f'Твои рефералы: {result_string} \n'
                                  f'Ожидаемы бонус: {bonus_1} ₽\n'
                                  f'Бонус за заявку: 0 ₽\n'
                                  f'Бонус за ипотеку:  0 ₽ ')
