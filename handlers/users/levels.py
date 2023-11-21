from utils.db_api.users_commands import save_count_levels, get_who_invited
from loader import dp, bot


async def set_levels(user_id_which):
    user_id_1 = await get_who_invited(user_id_which)
    user_id_2 = await get_who_invited(user_id_1)
    user_id_3 = await get_who_invited(user_id_2)
    user_id_4 = await get_who_invited(user_id_3)
    user_id_5 = await get_who_invited(user_id_4)

    if user_id_1 != '0' and user_id_1 is not None:
        await dp.bot.send_message(user_id_1, f'🟢 У тебя новая регистрация в 2 линии , твой "Ожидаемый бонус" 200 ₽')
        await save_count_levels(user_id_1, 2)
    if user_id_2 != '0' and user_id_2 is not None:
        await dp.bot.send_message(user_id_2, f'🟢 У тебя новая регистрация в 3 линии , твой "Ожидаемый бонус" 200 ₽')
        await save_count_levels(user_id_2, 3)
    if user_id_3 != '0' and user_id_3 is not None:
        await dp.bot.send_message(user_id_3, f'🟢 У тебя новая регистрация в 4 линии , твой "Ожидаемый бонус" 200 ₽')
        await save_count_levels(user_id_3, 4)
    if user_id_4 != '0' and user_id_4 is not None:
        await dp.bot.send_message(user_id_4, f'🟢 У тебя новая регистрация в 5 линии , твой "Ожидаемый бонус" 200 ₽')
        await save_count_levels(user_id_4, 5)

