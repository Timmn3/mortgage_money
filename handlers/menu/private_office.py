from aiogram.utils.deep_linking import get_start_link

from filters.subscription import subscriber
from loader import dp
from aiogram import types
from utils.db_api.users_commands import get_user_referrals, get_user_balance, get_usernames, get_bonus_1_value


@dp.callback_query_handler(text='Личный кабинет')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        ref_link = await get_start_link(payload=call.from_user.id)
        refs = await get_user_referrals(call.from_user.id)
        if not refs:
            usernames = 'у Вас нет рефералов'
        else:
            usernames = await get_usernames(refs)

        bonus_1 = await get_bonus_1_value(call.from_user.id)
        await call.message.answer(f'Твоя реферальная ссылка: \n{ref_link} \n'
                                  f'Твои рефералы: {usernames} \n'
                                  f'Ожидаемы бонус: {bonus_1} ₽')
