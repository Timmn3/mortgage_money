from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from data.config import help_user
from loader import dp
from utils.db_api.proposal_commands import get_proposal_data
from utils.db_api.users_commands import get_user_city_and_telephone


@dp.message_handler(text="/help")
async def command_help(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! \n'
                         f'Тебе нужна помощь? Напиши в техподдержку {help_user}')



