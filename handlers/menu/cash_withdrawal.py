from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bot_send.notify_admins import send_admins
from filters.subscription import subscriber
from loader import dp
from aiogram import types

from utils.db_api.users_commands import get_user_balance


class Balance(StatesGroup):
    amount = State()  # сумма
    requisites = State()  # реквизиты


@dp.callback_query_handler(text='Вывод средств')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        balance = await get_user_balance(call.from_user.id)
        await call.message.answer(f'Ваш баланс: {balance} ₽\n'
                                  f'введите сумму, которую хотите вывести:')
        await Balance.amount.set()


@dp.message_handler(state=Balance.amount)
async def process_cash_withdrawal(message: types.Message, state: FSMContext):
    amount_str = message.text
    # Проверяем, является ли введенная строка числом
    if amount_str.isdigit():
        amount = int(amount_str)
        await state.update_data(amount=amount)
        await message.answer("Введите реквизиты Вашего счета:")
        await Balance.requisites.set()
    else:
        await message.answer("Введите число!!!")


@dp.message_handler(state=Balance.requisites)
async def process_cash_withdrawal(message: types.Message, state: FSMContext):
    requisites = message.text
    data = await state.get_data()
    amount = data['amount']
    user = message.from_user.id
    await send_admins(dp, f'Пользователь {user} запросил вывод средств на сумму {amount} ₽ \n'
                          f'Реквизиты счета: {requisites}')
    await state.finish()
