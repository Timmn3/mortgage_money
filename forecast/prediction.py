import random
from loguru import logger
from data.config import numder_1_20
from utils.db_api.analisis_commands import select_analysis
from utils.db_api.circ_commands import count_edition, select_field


# просмотр выбранного количества (analys_number) крайних тиражей поля field
async def some_editions(field):
    try:
        last_number = await count_edition()
        analys_number = await select_analysis()
        draw_list = []
        for i in range(last_number - analys_number, last_number):
            k = await select_field(str(i + 1), field)
            if k is not None:
                draw_list.append(k)
        return draw_list
    except Exception as e:
        logger.error(f"Произошла ошибка в функции some_editions: {e}")


# статистика выпадения шаров за выбранное количество тиражей
async def statistics(field):
    try:
        draw_list = await some_editions(field)  # получаем список с n количеством тиражей по полю 1
        stat_dict = {}  # словарь для запись статистики по номерам
        # заполняем словарь значениями от 01 до 20
        for num in numder_1_20:
            stat_dict[num] = 0

        # проходим по всем выбранным тиражам и собираем статистику
        for num in numder_1_20:
            i = 0
            for draw in draw_list:
                if num in draw:
                    i += 1
            stat_dict[num] = i*10
            # удаляем все значения если выпало меньше 50%
            # if i < 5:
            #     del stat_dict[num]

        sorted_dict = dict(sorted(stat_dict.items(), reverse=True, key=lambda x: x[1]))  # Сортировка словаря по значению
        # достаем из словаря числа и проценты
        *numbers, = sorted_dict
        *percent, = sorted_dict.values()

        return numbers, percent
    except Exception as e:
        logger.error(f"Произошла ошибка в функции statistics: {e}")


# форматирование из списка в строку с разделителями
async def format_statistic(field):
    numbers, percent = await statistics(field)
    return "    ".join(numbers), "% ".join(map(str, percent))


# прогноз выдаем 4 числа
async def statistics_4(field):
    try:
        numbers, percent = await statistics(field)  # статистика по полю

        # функция формирования списка для прогноза
        def list_result(list_numbers):
            # значения для сравнения
            per = [60, 70, 80, 90, 100]
            # Количество чисел больше 60
            number_up_60 = 0
            result = []
            # смотрим количество вхождений per в список вероятностей percent и записываем в number_up_60
            # (т.е.все что >=60%)
            for word1 in per:
                for word2 in percent:
                    if word1 == word2:
                        number_up_60 += 1

            # делаем срез list_numbers по количеству вхождений number_up_60 т.е. >=60% и записываем в list_up_60
            list_up_60 = list_numbers[:number_up_60]
            # формируем result
            if number_up_60 > 0:
                if number_up_60 == 1:
                    result += list_numbers[:number_up_60]  # записываем 1 значение
                else:
                    result += random.sample(list_up_60, 2)  # 2 значения
            # добираем оставшиеся числа до 4
            result += random.sample(list_numbers[number_up_60:], 4 - len(result))

            return result

        # список выбираем 2 значения из списка >=60% и 2 рандомных
        result_1 = list_result(numbers)

        # формируем в список numbers_2 числа из numbers, которые не вошли в result
        for numb in result_1:
            if numb in numbers:
                percent.pop(numbers.index(numb))  # удаляем из списка процентов по индексу numbers
                numbers.remove(numb)

        # список (из не попавших в result) выбираем все значения из списка >60% и если что осталось то рандом
        result_2 = list_result(numbers)

        return " ".join(result_1), " ".join(result_2)
    except Exception as e:
        logger.error(f"Произошла ошибка в функции statistics_4: {e}")
