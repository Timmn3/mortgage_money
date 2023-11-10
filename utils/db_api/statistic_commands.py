from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.shemas.statistic import Statistic


# добавление
async def add_statistic(circulation: int, prediction_1: str, prediction_2: str, coincidence: str):
    try:
        statistic = Statistic(circulation=circulation, prediction_1=prediction_1, prediction_2=prediction_2,
                              coincidence=coincidence)
        await statistic.create()
    except UniqueViolationError:
        logger.info(f'Статистика тиража {circulation} не добавлена')


# выбрать тираж
async def select_circulation(circulation):
    circ = await Statistic.query.where(Statistic.circulation == circulation).gino.first()
    return circ


# функция изменения поля coincidence
async def change_coincidence(circulation: int, data):
    try:
        circ = await select_circulation(circulation)
        await circ.update(coincidence=data).apply()
    except Exception as e:
        logger.info(f'Нет тиража для записи: {e}')


# выбрать prediction_1 из тиража
async def select_prediction_1(circulation):
    number = await Statistic.select('prediction_1').where(Statistic.circulation == circulation).gino.scalar()
    return number


# выбрать prediction_2 из тиража
async def select_prediction_2(circulation):
    number = await Statistic.select('prediction_2').where(Statistic.circulation == circulation).gino.scalar()
    return number
