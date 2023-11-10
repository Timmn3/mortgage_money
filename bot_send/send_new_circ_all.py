from asyncio import sleep

from data.config import admins
from forecast.coincidence import prediction_matches
from forecast.prediction import statistics_4, format_statistic
from keyboards.inline.buy_ticket import ikb_buy_ticket
from loader import dp
from parser.rezult import parse_rezult
from utils.db_api import user_commands as commands, circ_commands
from utils.db_api.circ_commands import count_edition
from utils.db_api.statistic_commands import add_statistic
# отправить сообщение с последним тиражом
from utils.db_api.user_commands import change_balance


# прогноз на следующий тираж 4 числа
async def forecast_for_next_draw():
    circ = await count_edition()  # Крайний тираж
    numbers_1_1, numbers_1_2 = await statistics_4(1)  # статистика по полю 1
    numbers_2_1, numbers_2_2 = await statistics_4(2)  # статистика по полю 2
    field_1 = f'<b>Поле 1:</b>\n номера:  <b>{numbers_1_1}</b>  ({numbers_1_2})'
    field_2 = f'<b>Поле 2:</b>\n номера:  <b>{numbers_2_1}</b>  ({numbers_2_2})'
    # записываем прогноз в БД
    await add_statistic(circulation=circ + 1, prediction_1=numbers_1_1 + ' ' + numbers_1_2,
                        prediction_2=numbers_2_1 + ' ' + numbers_2_2, coincidence='')
    return field_1, field_2


async def check_circulation():
    circ = await count_edition()  # Крайний тираж
    numbers_drawn = await circ_commands.select_edition(str(circ))  # выпавшие числа
    numbers_drawn_1 = str(numbers_drawn[0])  # достаем первый ряд выпавших чисел из списка
    numbers_drawn_2 = str(numbers_drawn[1])  # достаем второй ряд выпавших чисел из списка
    date = str(numbers_drawn[2])  # достаем время тиража
    # все пользователи из БД c балансом больше 9 руб
    users = await commands.select_all_users_big_balance()
    # прогноз на следующий тираж 4 числа
    field_1, field_2 = await forecast_for_next_draw()
    # совпадения предсказания с выпавшими числами
    prediction, prediction_2 = await prediction_matches(circ, numbers_drawn_1, numbers_drawn_2)

    text = f'❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️' \
           f'\n<b>Тираж № {circ} от {date}</b>\nВыпавшие числа:\n<b>{numbers_drawn_1}</b>  <b>{numbers_drawn_2}</b>'
    win = await parse_rezult(circ, prediction)
    win_2 = await parse_rezult(circ, prediction_2)

    for user in users:
        try:
            await change_balance(user.user_id, -2.5)  # снимаем сумму с баланса
            await dp.bot.send_message(chat_id=user.user_id, text=text)  # выпавшие числа
            await dp.bot.send_message(chat_id=user.user_id, text=f'Угадано чисел в тираже <b>№{circ}</b>\n'
                                                                 f'в 1-м и 2-м поле: '
                                                                 f'<b> {prediction}</b> ({prediction_2})     ✅\n'
                                                                 f'Выигрыш составил: <b>{win} ₽</b> ({win_2} ₽)')
            await dp.bot.send_message(chat_id=user.user_id, text=f'👉<b>Прогноз на тираж №{circ + 1}:</b>')
            await dp.bot.send_message(chat_id=user.user_id, text=field_1)
            await dp.bot.send_message(chat_id=user.user_id, text=field_2, reply_markup=ikb_buy_ticket)
            await sleep(0.25)  # 4 сообщения в секунду
        except Exception:
            pass


async def send_statistic():
    # отправить админам статистику
    numbers_1, percent_1 = await format_statistic(1)  # статистика по полю 1
    numbers_2, percent_2 = await format_statistic(2)  # статистика по полю 2
    # Крайний тираж
    last = await count_edition()
    for admin in admins:
        await dp.bot.send_message(chat_id=admin, text=f'<b>📍Статистика, следующий тираж №{last + 1}:</b>\n')
        await dp.bot.send_message(chat_id=admin, text=f'<b>Поле 1:</b>\nномера:  <b>{numbers_1}</b>\n'
                                                      f'процент: {percent_1}%')
        await dp.bot.send_message(chat_id=admin, text=f'<b>Поле 2:</b>\nномера:  <b>{numbers_2}</b>\n'
                                                      f'процент: {percent_2}%')
