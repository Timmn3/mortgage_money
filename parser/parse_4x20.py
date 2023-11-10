from bs4 import BeautifulSoup
import requests


def parse_4x20():
    # парсинг сохраненной страницы
    # with open(f'c:/Users/RedmiBookUser/PycharmProjects/Написанные/Телеграмм/стол/parser/4x20.html',
    #           encoding="utf-8") as file:
    #     src = file.read()
    # soup = BeautifulSoup(src, 'lxml')

    # парсинг с сайта страницы (50 последних тиражей)
    url = 'https://www.stoloto.ru/4x20/archive'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    circulation = soup.find_all(class_='draw')  # № тиража
    balls = soup.find_all(class_='container cleared')  # выпавшая комбинация
    f = open('4x20.txt', 'w')

    for i in range(2, len(circulation)):
        circ = circulation[i].text.replace('\n', '')  # убираем символы \n
        ball = balls[i - 2].text.replace('\n', '')
        list_b_1 = []
        list_b_2 = []
        for j in range(0, 8, 2):
            list_b_1.append(ball[j:j + 2])
        ball_1 = ''.join(sorted(list_b_1))  # .join из списка в строку sorted - сортируем по порядку
        for j in range(8, 16, 2):
            list_b_2.append(ball[j:j + 2])
        ball_2 = ''.join(sorted(list_b_2))

        #  записываем в массив
        tupl = circ
        f.write(tupl + ball_1 + ball_2 + '\n')
    f.close()


print(parse_4x20())
