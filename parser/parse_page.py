import requests
from bs4 import BeautifulSoup

from bot_send.notify_admins import send_admins
from bot_send.send_new_circ_all import check_circulation
from loader import dp
from utils.db_api import circ_commands as commands
from utils.db_api.circ_commands import count_edition
from utils.db_api.start_stop_commands import select_start_stop


async def parse_page():
    url = 'https://www.stoloto.ru/4x20/archive'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    date_time = soup.find_all(class_='draw_date')  # дата тиража
    circulation = soup.find_all(class_='draw')  # № тиража
    balls = soup.find_all(class_='container cleared')  # выпавшая комбинация
    circ_list = []

    # парсим данные последнего тиража
    circ_last = int(circulation[2].text.strip())  # убираем символы в начале и в конце
    # количество тиражей в БД
    circ_count = int(await count_edition())
    # если тираж уже есть в БД
    if circ_last <= circ_count:
        text = f'Тираж {circ_last} уже есть❗'
        await send_admins(dp, text)
    else:
        for i in range(len(circulation)-1, 1, -1):
            circ = circulation[i].text.strip()  # убираем символы в начале и в конце
            date = date_time[i-1].text
            # strip() - убираем любые символы в начале и конце, [:11] - делаем срез, .split() -  из строки в список
            try:
                balls_1_list = balls[i - 2].text.strip().replace('\n', ' ')[:11].split()
                balls_2_list = balls[i - 2].text.strip().replace('\n', ' ')[-11:].split()
                balls_1 = " ".join(sorted(balls_1_list)) + ' '  # .join из списка в строку sorted - сортируем по порядку
                balls_2 = " ".join(sorted(balls_2_list)) + ' '
                #  записываем в массив
                tupl = (circ, date, balls_1, balls_2)
                circ_list.append(tupl)
            except Exception as e:
                print(e)
        return circ_list


async def add_in_bd_page():
    # если прогнозы запущены
    if await select_start_stop() == 'True':
        # парсим страницу
        circ_list = await parse_page()
        # добавляем тиражи в БД
        if circ_list:
            for circ in range(len(circ_list)):
                await commands.add_edition(circulations=circ_list[circ][0], date=circ_list[circ][1],
                                           balls_1=circ_list[circ][2], balls_2=circ_list[circ][3])
            # отправить пользователям сообщение с последним тиражом
            await check_circulation()
            # отправить админам статистику

