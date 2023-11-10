import requests
from bs4 import BeautifulSoup
from utils.db_api import circ_commands as commands

# парсим только последний тираж
async def parse_last():
    url = 'https://www.stoloto.ru/4x20/archive'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    date_time = soup.find_all(class_='draw_date')  # дата тиража
    circulation = soup.find_all(class_='draw')  # № тиража
    balls = soup.find_all(class_='container cleared')  # выпавшая комбинация
    i = 2
    # парсим только данные последнего тиража
    circ = circulation[i].text.strip()  # убираем символы в начале и в конце
    date = date_time[i - 1].text
    # strip() - убираем любые символы в начале и конце, [:11] - делаем срез, .split() - преобразуем из строки в список
    balls_1_list = balls[i - 2].text.strip().replace('\n', ' ')[:11].split()
    balls_2_list = balls[i - 2].text.strip().replace('\n', ' ')[-11:].split()
    balls_1 = " ".join(sorted(balls_1_list)) + ' '  # .join из списка в строку sorted - сортируем по порядку
    balls_2 = " ".join(sorted(balls_2_list)) + ' '
    print(f'{date} тираж № {circ}\nВыпавшая комбинация: {balls_1} {balls_2}')

    await commands.add_edition(circulations=circ, date=date, balls_1=balls_1, balls_2=balls_2)




