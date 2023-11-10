from filters import Admins_message
from forecast.prediction import format_statistic
from parser.parse_page import add_in_bd_page
from states import Analysis, User_balance, Send_messsage
from utils.db_api.analisis_commands import select_analysis, change_analysis
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from utils.db_api import user_commands as commands
from asyncio import sleep


# вывод команд для админа
from utils.db_api.circ_commands import count_edition
from utils.db_api.start_stop_commands import change_start_stop
from utils.db_api.user_commands import change_balance, user_balance


@dp.message_handler(Admins_message(), Command('admin'))
async def req(message: types.Message):
    await message.answer(f'/req парсинг последнего тиража\n'
                         f'/analysis количество тиражей для анализа прогноза\n'
                         f'/change_balance изменение баланса пользователя\n'
                         f'/statistics статистика выпадений (прогноз)\n'
                         f'/message отправить сообщения всем пользователям\n'
                         f'/stop остановить прогнозы\n'
                         f'/starting запустить прогнозы')

# Если команда /request
@dp.message_handler(Admins_message(), Command('req'))
async def req(message: types.Message):
    # Парсинг последнего тиража
    await add_in_bd_page()

# останавливаем прогнозы
@dp.message_handler(Admins_message(), Command('stop'))
async def req(message: types.Message):
    await change_start_stop('False')
    await message.answer('Прогнозы остановлены')

# запускаем прогнозы
@dp.message_handler(Admins_message(), Command('starting'))
async def req(message: types.Message):
    await change_start_stop('True')
    await message.answer('Прогнозы запущены')

# загружает в файл количество тиражей для анализа прогноза
@dp.message_handler(Admins_message(), Command('analysis'))
async def req(message: types.Message):
    await message.answer(f'Кличество тиражей для анализа: {await select_analysis()}\n'
                         f'Введите новое значение:')
    await Analysis.amount.set()  # устанавливаем состояние

# Отлавливаем состояние введенного количество тиражей для анализа прогноза:
@dp.message_handler(state=Analysis.amount)
async def accept_reg(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        await change_analysis(amount)
        await message.answer('записано')
        await state.finish()
    except Exception:
        await message.answer('введите целое число:')


# изменить баланс юзеру
@dp.message_handler(Admins_message(), Command('change_balance'))
async def change_user_balance(message: types.Message):
    await message.answer(f'Введите user_id:')
    await User_balance.user_id.set()  # устанавливаем состояние

# Отлавливаем состояние введенного user_id
@dp.message_handler(state=User_balance.user_id)
async def user_id(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)  # записываем значение в data
    # какой баланс у пользователя
    balance = await user_balance(int(message.text))
    await message.answer(f'Баланс пользователя составляет {balance} ₽')
    await message.answer(f'Введите сумму пополнения:')
    await User_balance.amount.set()  # устанавливаем состояние

# Отлавливаем состояние введенной суммы
@dp.message_handler(state=User_balance.amount)
async def user_id(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)  # записываем значение в data
    data = await state.get_data()  # получаем в переменную список ответов
    try:
        user = int(data.get('user_id'))  # записываем ответы в переменные
        amount = int(data.get('amount'))
        # записываем в БД
        await change_balance(user, amount)
        # какой баланс
        balance = await user_balance(user)
        await message.answer(f'Баланс пользователя id: {user} равен {balance} ₽')
    except Exception:
        await message.answer('ошибка ввода данных, попробуйте снова /change_balance')
    await state.finish()  # обязательно завершаем состояни

async def admin_statistics(message: types.Message):
    numbers_1, percent_1 = await format_statistic(1)  # статистика по полю 1
    numbers_2, percent_2 = await format_statistic(2)  # статистика по полю 1
    # Крайний тираж
    last = await count_edition()
    await message.answer(f'<b>📍Статистика, следующий тираж №{last + 1}:</b>\n')
    await message.answer(f'<b>Поле 1:</b>\nномера:  <b>{numbers_1}</b>\nпроцент: {percent_1}%')
    await message.answer(f'<b>Поле 2:</b>\nномера:  <b>{numbers_2}</b>\nпроцент: {percent_2}%')

# Если команда /statistics
@dp.message_handler(Admins_message(), Command('statistics'))
async def req(message: types.Message):
    await admin_statistics(message)


# команда /message отправить сообщения всем пользователям
@dp.message_handler(Admins_message(), Command('message'))
async def send_message(message: types.Message):
    await message.answer('Какое сообщение отправить:')
    await Send_messsage.send_mess.set()  # устанавливаем состояние

# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=Send_messsage.send_mess)
async def send_message(message: types.Message, state: FSMContext):
    await send_mess(message.text)
    await message.answer('отправлено')
    await state.finish()

async def send_mess(message: types.Message):
    # все пользователи из БД
    users = await commands.select_all_users()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id, text=message)
            await sleep(0.25)  # 4 сообщения в секунду
        except Exception:
            pass
