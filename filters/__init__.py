from aiogram import Dispatcher
from .by_balance import PositiveBalance
from .subscription import IsSubscriber
from .admins import AdminsMessage


# функция, которая выполняет установку кастомных фильтов
def setup(dp: Dispatcher):
    dp.filters_factory.bind(PositiveBalance)  # кастомный фильтр для проверки на позитивный баланс
    dp.filters_factory.bind(IsSubscriber)  # проверка подписки на канал
    dp.filters_factory.bind(AdminsMessage)  # сообщения только для админов