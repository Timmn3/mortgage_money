from aiogram.dispatcher.filters.state import StatesGroup, State


class Circ_state(StatesGroup):
    circulations = State()

class Number_search(StatesGroup):
    number_search_1 = State()
    number_search_2 = State()
