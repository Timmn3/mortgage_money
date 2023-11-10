from utils.db_api.statistic_commands import select_prediction_1, select_prediction_2, change_coincidence


# совпадения предсказания с выпавшими числами

async def prediction_matches(circulation, numbers_drawn_1, numbers_drawn_2):  # передаем № тиража и выпавшие числа
    # предсказанные числа из предыдущего тиража, достаем из БД
    try:
        pred_numb_1 = (await select_prediction_1(circulation))[:11]
        pred_numb_2 = (await select_prediction_2(circulation))[:11]

        pred_numb_1_2 = (await select_prediction_1(circulation))[11:]
        pred_numb_2_2 = (await select_prediction_2(circulation))[11:]

        # из строки в список
        list_1 = numbers_drawn_1.split()  # ['12', '13', '14, '15']
        list_2 = numbers_drawn_2.split()

        # сравниваем числа на совпадение предсказанных с реальными
        field_1 = 0
        for i in list_1:
            if i in pred_numb_1:
                field_1 += 1

        field_2 = 0
        for i in list_2:
            if i in pred_numb_2:
                field_2 += 1

        data = str(field_1)+' и '+str(field_2)

        # сравниваем числа ряда 2 на совпадение предсказанных с реальными
        field_1_2 = 0
        for i in list_1:
            if i in pred_numb_1_2:
                field_1_2 += 1

        field_2_2 = 0
        for i in list_2:
            if i in pred_numb_2_2:
                field_2_2 += 1

        data_2 = str(field_1_2)+' и '+str(field_2_2)

        # записываем в БД совпадения 2и1 в текущий тираж
        await change_coincidence(circulation, f'{data} ({data_2})')
        return data, data_2

    except Exception as e:
        print(e)
        return '01 02 03 04', '01 02 03 04'


