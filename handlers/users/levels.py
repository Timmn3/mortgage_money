from utils.db_api.users_commands import find_user_by_referral_value
from loader import dp, bot


async def set_levels(user_id_which):
    user_id_1 = await find_user_by_referral_value(str(user_id_which))
    user_id_2 = await find_user_by_referral_value(str(user_id_1))
    user_id_3 = await find_user_by_referral_value(str(user_id_2))
    user_id_4 = await find_user_by_referral_value(str(user_id_3))
    user_id_5 = await find_user_by_referral_value(str(user_id_4))
    if user_id_1:
        await dp.bot.send_message(user_id_1, f'🟢 У тебя новая регистрация в 2 линии , твой "Ожидаемый бонус" 200 ₽')
    if user_id_2:
        await dp.bot.send_message(user_id_2, f'🟢 У тебя новая регистрация в 3 линии , твой "Ожидаемый бонус" 200 ₽')
    if user_id_3:
        await dp.bot.send_message(user_id_3, f'🟢 У тебя новая регистрация в 4 линии , твой "Ожидаемый бонус" 200 ₽')
    if user_id_4:
        await dp.bot.send_message(user_id_4, f'🟢 У тебя новая регистрация в 5 линии , твой "Ожидаемый бонус" 200 ₽')

