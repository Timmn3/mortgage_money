from filters.subscription import subscriber
from loader import dp
from aiogram import types

from utils.db_api.users_commands import get_bonus_1_value


@dp.callback_query_handler(text='Мои бонусы')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        bonus_1 = await get_bonus_1_value(call.from_user.id)
        await call.message.answer(f'Ожидаемы бонус: {bonus_1} ₽\n'
                                  f'Бонус за заявку: 0 ₽\n'
                                  f'Бонус за ипотеку:  0 ₽ ')
