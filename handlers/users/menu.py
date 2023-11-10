from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from bot_send.send_new_circ_all import forecast_for_next_draw
from filters import PositiveBalance, IsSubsriber
from forecast.prediction import statistics, statistics_4, format_statistic
from keyboards.inline import ikb_menu
from keyboards.inline.buy_ticket import ikb_buy_ticket
from loader import dp

from search.input_validation import validation
from states import Circ_state, Number_search
from utils.db_api import circ_commands
from utils.db_api.circ_commands import count_edition, combination_search_1, \
    combination_search_2


# Если команда menu , то выводи инлайн клавиатуру
@dp.message_handler(IsSubsriber(), Command('menu'))
async def menu(message: types.Message):
    await message.answer('Выберете один из пунктов меню:', reply_markup=ikb_menu)


# Количество тиражей
@dp.callback_query_handler(IsSubsriber(), text="Количество тиражей")
async def send_message(call: CallbackQuery):
    count = await count_edition()  # количество тиражей
    await call.message.answer(f'Количество тиражей: {count}\n')
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение 'Выберете один из пунктов меню:'


# Проверить тираж №
@dp.callback_query_handler(IsSubsriber(), text='Проверить тираж №')
async def accept_reg(call: types.CallbackQuery):
    await call.message.answer('Введите номер тиража:')
    await Circ_state.circulations.set()
    await call.message.edit_reply_markup()
    await call.message.delete()  # удаляем сообщение 'Выберете один из пунктов меню:'


# Отлавливаем состояние введенного номера тиража:
@dp.message_handler(state=Circ_state.circulations)
async def accept_reg(message: types.Message, state: FSMContext):
    circ = message.text  # выбранный тираж
    numbers_drawn = await circ_commands.select_edition(circ)  # выпавшие числа
    numbers_drawn_1 = str(numbers_drawn[0])  # достаем первый ряд выпавших чисел из списка
    numbers_drawn_2 = str(numbers_drawn[1])  # достаем второй ряд выпавших чисел из списка
    date = str(numbers_drawn[2])  # достаем время тиража

    if numbers_drawn_1 == 'None':
        await message.answer('Тираж не найден, попробуйте снова:', reply_markup=ikb_menu)
    else:
        await message.answer(f'Тираж № {circ} от {date} \nВыпавшие числа:\n<b>{numbers_drawn_1}</b>  '
                             f'<b>{numbers_drawn_2}</b>')
    await state.finish()


# Поиск комбинации
@dp.callback_query_handler(IsSubsriber(), text='Поиск комбинации')
async def accept_reg(call: types.CallbackQuery):
    await call.message.answer('Введите не более 4-х чисел через пробел (например 03 11 19):')
    await call.message.answer('<b>Поле 1:</b>')
    await Number_search.number_search_1.set()  # устанавливаем состояние для первой комбинации
    await call.message.edit_reply_markup()
    await call.message.delete()  # удаляем сообщение 'Выберете один из пунктов меню:'


# Отлавливаем состояние первой введенной комбинации
@dp.message_handler(state=Number_search.number_search_1)
async def accept_reg(message: types.Message, state: FSMContext):
    await state.update_data(number_search_1=message.text)  # записываем значение в data
    await message.answer('<b>Поле 2:</b>')  # отправляем сообщение о вводе второй комбинации
    await Number_search.number_search_2.set()  # устанавливаем состояние для второй комбинации


# Отлавливаем состояние второй введенной комбинации
@dp.message_handler(state=Number_search.number_search_2)
async def accept_reg(message: types.Message, state: FSMContext):
    await state.update_data(number_search_2=message.text)  # записываем значение в data
    data = await state.get_data()  # получаем в переменную список ответов
    number_search_1 = data.get('number_search_1')  # записываем ответы в переменные
    number_search_2 = data.get('number_search_2')
    await state.finish()  # обязательно завершаем состояние
    output_1 = validation(number_search_1)
    output_2 = validation(number_search_2)

    if output_1.replace(' ', '').isdigit():
        output_1 = len(await combination_search_1(output_1))
        only_numb_1 = True
    else:
        only_numb_1 = False
    if output_2.replace(' ', '').isdigit():
        output_2 = len(await combination_search_2(output_2))
        only_numb_2 = True
    else:
        only_numb_2 = False
    # если введены правильно комбинации
    if only_numb_1 and only_numb_2:
        await message.answer(f'<b>Поле 1: \n комбинация: </b>{number_search_1} \n'
                             f'встречалась в {output_1} тиражах\n'
                             f'<b>Поле 2: \n комбинация: </b>{number_search_2} \n'
                             f'встречалась в {output_2} тиражах')
    # иначе вывод ошибки
    else:
        await message.answer(f'<b>Поле 1: </b>{number_search_1} ({output_1})\n'
                             f'<b>Поле 2: </b>{number_search_2} ({output_2})')

async def prognosis(message: types.Message):
    # прогноз на следующий тираж 4 числа
    circ = await count_edition()  # Крайний тираж
    field_1, field_2 = await forecast_for_next_draw()
    await message.answer(f'👉<b>Прогноз на тираж №{circ + 1}:</b>')
    await message.answer(field_1)
    await message.answer(field_2, reply_markup=ikb_buy_ticket)

@dp.callback_query_handler(PositiveBalance(), IsSubsriber(), text="Прогноз")
async def send_message(call: CallbackQuery):
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение 'Выберете один из пунктов меню:'
    await prognosis(call.message)


