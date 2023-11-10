from bs4 import BeautifulSoup
from utils.db_api import circ_commands as commands

# парсим все на странице
def parse_all():
    # открыть сохраненную страницу
    with open(f'c:/Users/RedmiBookUser/PycharmProjects/Написанные/Телеграмм/стол/parser/Архив.html', encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    date_time = soup.find_all(class_='draw_date')  # дата тиража
    circulation = soup.find_all(class_='draw')  # № тиража
    balls = soup.find_all(class_='container cleared')  # выпавшая комбинация

    circ_list = []
    for i in range(len(circulation)-1, 1, -1):
        circ = circulation[i].text.strip()  # убираем символы в начале и в конце
        date = date_time[i-1].text
        # strip() - убираем любые символы в начале и конце, [:11] - делаем срез, .split() -  из строки в список
        balls_1_list = balls[i - 2].text.strip().replace('\n', ' ')[:11].split()
        balls_2_list = balls[i - 2].text.strip().replace('\n', ' ')[-11:].split()
        balls_1 = " ".join(sorted(balls_1_list)) + ' '  # .join из списка в строку sorted - сортируем по порядку
        balls_2 = " ".join(sorted(balls_2_list)) + ' '
        #  записываем в массив
        tupl = (circ, date, balls_1, balls_2)
        circ_list.append(tupl)
    return circ_list

async def add_in_bd_all(circ_list):
    for circ in range(len(circ_list)):
        await commands.add_edition(circulations=circ_list[circ][0], date=circ_list[circ][1],
                                   balls_1=circ_list[circ][2], balls_2=circ_list[circ][3])
