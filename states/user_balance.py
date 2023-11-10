from aiogram.dispatcher.filters.state import StatesGroup, State


class User_balance(StatesGroup):
    user_id = State()
    amount = State()

