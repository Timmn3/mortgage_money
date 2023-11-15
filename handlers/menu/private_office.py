from aiogram.utils.deep_linking import get_start_link
from loader import dp
from aiogram import types
from utils.db_api.users_commands import get_user_referrals, get_user_balance


@dp.callback_query_handler(text='Личный кабинет')
async def accept_reg(call: types.CallbackQuery):
    ref_link = await get_start_link(payload=call.from_user.id)
    refs = await get_user_referrals(call.from_user.id)
    if not refs:
        refs = 'у Вас нет рефералов'
    balance = await get_user_balance(call.from_user.id)
    await call.message.answer(f'Твоя реферальная ссылка: \n{ref_link} \n'
                              f'Твои рефералы: {refs} \n'
                              f'Баланс: {balance} ₽')
