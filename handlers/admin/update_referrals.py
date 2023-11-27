""" Проходит по всем user_id и обновляет список количества рефералов"""

from filters import AdminsMessage
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command

from utils.db_api.users_commands import reset_all_user_data, save_count_levels, \
    get_user_id_who_invited_dict


# команда /update_referrals
@dp.message_handler(AdminsMessage(), Command('update_referrals'))
async def send_message(message: types.Message):
    await message.answer('Подождите...')
    await reset_all_user_data()
    dict_users = await get_user_id_who_invited_dict()

    for user in dict_users:
        await calculate_levels(dict_users, user)

    await message.answer('Данные по рефералам обновлены')


async def calculate_levels(dictionary, user_0):
    levels = [0, 0, 0, 0, 0]
    # список ключей у данного юзера
    keys_list_0 = find_keys_by_value(dictionary, user_0)
    levels[0] += len(keys_list_0)
    # print(keys_list_0)
    for user_1 in keys_list_0:
        await save_count_levels(user_0, 1)
        keys_list_1 = find_keys_by_value(dictionary, user_1)
        levels[1] += len(keys_list_1)
        # if user_1:
        #     print(f'{user_1}: {keys_list_1}')
        for user_2 in keys_list_1:
            keys_list_2 = find_keys_by_value(dictionary, user_2)
            levels[2] += len(keys_list_2)
            await save_count_levels(user_0, 2)
            # if user_2:
            #     print(f'{user_2}: {keys_list_2}')
            for user_3 in keys_list_2:
                keys_list_3 = find_keys_by_value(dictionary, user_3)
                levels[3] += len(keys_list_3)
                await save_count_levels(user_0, 3)
                # if user_3:
                #     print(f'{user_3}: {keys_list_3}')
                for user_4 in keys_list_3:
                    keys_list_4 = find_keys_by_value(dictionary, user_4)
                    levels[4] += len(keys_list_4)
                    await save_count_levels(user_0, 4)
                    # if user_4:
                    #     print(f'{user_4}: {keys_list_4}')
                    for user_5 in keys_list_4:
                        await save_count_levels(user_0, 5)

    return levels


def find_keys_by_value(dictionary, target_value):
    """ Ищем все вхождения users в value """
    keys_list = [key for key, value in dictionary.items() if value == target_value]
    return keys_list
