import datetime
from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline import ikb_balance, ikb_replenish_the_balance
from keyboards.inline.ikb_balance import ikb_check_payment
from loader import dp
from states import Balance
from utils.db_api import user_commands as commands
from utils.db_api.user_commands import change_bill_id, user_bill_id, clear_bill_id, change_balance
from utils.misc.qiwi import payment, payment_verification, cancel_payment, amount_of_payment


@dp.message_handler(Command('balance'))  # по каманде /balance выводит баланс
async def show_balance(message: types.Message):
    balance = await commands.user_balance(int(message.from_user.id))
    await message.answer(f'Ваш баланс: {balance} ₽', reply_markup=ikb_balance)


# пользователь нажал пополнить
@dp.callback_query_handler(text="Пополнить")
async def send_message(call: CallbackQuery):
    await call.message.answer('Тарифы:\n'
                              'посуточно - 10 ₽/день\n'
                              'на 30 дней - 200 ₽',
                              reply_markup=ikb_replenish_the_balance)
    # если пользователь снова нажимает пополнить, то удаляем прошлый платеж
    try:
        bill_id = await user_bill_id(call.from_user.id)  # получаем идентификатор заказа из БД
        await cancel_payment(bill_id=bill_id)  # закрываем счет на оплату
        await clear_bill_id(int(call.from_user.id))  # очищаем идентификатор заказа в БД
    except Exception:
        pass
    await call.message.edit_reply_markup()  # убрать клавиатуру


# функция создания идентификатора заказа
async def create_bill_id(user_id, amount):
    dt_now = datetime.datetime.now()  # текущее время
    bill_id = str(user_id) + str(dt_now)  # идентификатор заказа
    await change_bill_id(user_id, bill_id)  # записали в БД идентификатор заказа
    link = await payment(bill_id=bill_id, amount=amount)  # ссылка на оплату в qiwi
    return link


# пользователь нажал 200 ₽
@dp.callback_query_handler(text="200")
async def send_message(call: CallbackQuery):
    link = await create_bill_id(user_id=call.from_user.id, amount=200)
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.answer(f'Ссылка для пополнение баланса: \n{link}')
    await call.message.answer('Нажмите, что бы проверить или отменить оплату:', reply_markup=ikb_check_payment)


# пользователь нажал другая сумма
@dp.callback_query_handler(text="другая сумма")
async def send_message(call: CallbackQuery):
    await call.message.answer('Введите сумму пополнения:')
    await Balance.amount.set()
    await call.message.edit_reply_markup()  # убрать клавиатуру


# отлавливаем введенное значение для оплаты
@dp.message_handler(state=Balance.amount)
async def change_balances(message: types.Message, state: FSMContext):
    amount = message.text  # сумма пополнения
    try:
        if int(amount):
            if int(amount) >= 10:
                link = await create_bill_id(user_id=message.from_user.id, amount=amount)
                await message.answer(f'Ссылка для пополнение баланса: \n{link}')
                await message.answer('Нажмите, что бы проверить или отменить оплату:', reply_markup=ikb_check_payment)
                await state.finish()  # завершаем состояние
    except Exception:
        await message.answer('Введите целое число, минимальная сумма 10 ₽')
        await Balance.amount.set()


async def check_status(message):
    status = 'Не определен'
    if message == 'REJECTED':
        status = 'Платеж отклонен'
    if message == 'WAITING':
        status = 'Платеж в ожидании оплаты'
    if message == 'EXPIRED':
        status = 'Истекло время ожидания платежа'
    if message == 'PAID':
        status = 'Оплачено'
    return status


# проверка оплаты
# пользователь нажал проверить
@dp.callback_query_handler(text="проверить")
async def send_message(call: CallbackQuery):
    user_id = int(call.from_user.id)
    bill_id = await user_bill_id(user_id)  # получаем идентификатор заказа из БД
    status = await payment_verification(bill_id=bill_id)  # Проверим статус выставленного счета
    status = await check_status(status)
    await call.message.answer(f'Ваш статус: {status}')
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение
    if status == 'Оплачено':
        amount = await amount_of_payment(bill_id)  # проверяем сумму по запросу qiwi
        if float(amount) == 200.00:  # при пополнении баланса на 200 на счет заносится 300
            await change_balance(user_id, 300)  # заносим сумму в БД
        else:
            await change_balance(user_id, amount)  # заносим сумму в БД
        balance = await commands.user_balance(user_id)  # смотрим какая в БД сумма
        await call.message.answer(f'Ваш баланс: {balance} ₽')
        await clear_bill_id(user_id)  # очищаем идентификатор заказа в БД
    else:
        await call.message.answer(f'Попробуйте оплатить снова, после нажмите проверить:',
                                  reply_markup=ikb_check_payment)


# пользователь нажал отменить
@dp.callback_query_handler(text="отменить")
async def send_message(call: CallbackQuery):
    bill_id = await user_bill_id(call.from_user.id)  # получаем идентификатор заказа из БД
    await cancel_payment(bill_id=bill_id)  # закрываем счет на оплату
    await clear_bill_id(int(call.from_user.id))  # очищаем идентификатор заказа в БД
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение

# рассылает сообщение у кого баланс ниже установленного
async def send_message_users_balance_lower_100():
    # все пользователи из БД c балансом ниже 30
    users = await commands.select_all_users_balance_lower_100()
    for user in users:
        balance = await commands.user_balance(int(user.user_id))
        if balance > 9:
            text = f'Сумма на Вашем счету: {balance} ₽\n' \
                   f'При балансе менее 10 ₽ Вы не сможете пользоваться всеми функциями'
            try:
                await dp.bot.send_message(chat_id=user.user_id, text=text, reply_markup=ikb_balance)
                await sleep(0.25)  # 4 сообщения в секунду
            except Exception:
                pass