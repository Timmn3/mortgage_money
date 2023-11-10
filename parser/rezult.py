import requests
from bs4 import BeautifulSoup

async def parse_rezult(circ, comb):
    url = f'https://www.stoloto.ru/4x20/archive/{circ}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('td')  # дата тиража
    result = '0'

    if comb == '4 и 4':
        result = data[67].text.strip()
    if comb == '4 и 3' or comb == '3 и 4':
        result = data[8].text.strip()
        if result == '0':
            result = '200000'
    if comb == '4 и 2' or comb == '2 и 4':
        result = data[13].text.strip()
        if result == '0':
            result = '50000'
    if comb == '4 и 1' or comb == '1 и 4':
        result = data[18].text.strip()
        if result == '0':
            result = '10000'
    if comb == '4 и 0' or comb == '0 и 4':
        result = data[23].text.strip()
        if result == '0':
            result = '10000'
    if comb == '3 и 3':
        result = data[28].text.strip()
        if result == '0':
            result = '3000'
    if comb == '3 и 2' or comb == '2 и 3':
        result = data[33].text.strip()
        if result == '0':
            result = '2000'
    if comb == '3 и 1' or comb == '1 и 3':
        result = data[38].text.strip()
        if result == '0':
            result = '1000'
    if comb == '3 и 0' or comb == '0 и 3':
        result = data[43].text.strip()
        if result == '0':
            result = '1000'
    if comb == '2 и 2':
        result = data[48].text.strip()
    if comb == '2 и 1' or comb == '1 и 2':
        result = data[53].text.strip()
    if comb == '2 и 0' or comb == '0 и 2':
        result = data[58].text.strip()

    return result
