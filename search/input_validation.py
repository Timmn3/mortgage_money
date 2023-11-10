from data.config import numder_1_20


def validation(inp: str):
    if len(inp) > 11:
        return 'Ошибка! Количество символов должно быть меньше 11!'
    elif len(inp) < 2:
        return 'Ошибка! Количество символов должно быть больше 2'
    elif not inp.replace(' ', '').isdigit():
        return 'Ошибка! Должны быть только цифры'
    else:
        if repeat_num(inp) == 'повтор':
            return 'Ошибка ввода'
        else:
            return repeat_num(inp)


# функция для приведения к правильной форме
def num(inp):
    inp = inp.replace(' ', '')  # убираем пробелы
    list_num = []
    if len(inp) % 2 == 0:  # проверяем на четность
        while len(inp) > 0:
            slice_num = inp[:2]
            if slice_num not in numder_1_20:
                return False
            else:
                list_num.append(slice_num)  # делаем срез по 2 цифры и записываем в список
                inp = inp[2:]
        return list_num
    else:
        return False

# провераем на повторяющиеся цифры
def repeat_num(inp):
    nums = num(inp)
    try:
        line = " ".join(sorted(nums))  # .join из списка в строку sorted - сортируем по порядку
    except Exception:
        line = 'Ошибка ввода'
    line_0 = 'повтор'
    visited = set()
    try:
        dup = [x for x in nums if x in visited or (visited.add(x) or False)]
        if dup:
            return line_0
        else:
            return line
    except Exception:
        return 'Ошибка введенных значений'
