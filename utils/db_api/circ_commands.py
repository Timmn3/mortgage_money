from asyncpg import UniqueViolationError
from loguru import logger
from bot_send.notify_admins import send_admins
from utils.db_api.db_gino import db
from utils.db_api.shemas.edition import Edition
import datetime


# добавление тиражей
async def add_edition(circulations: str, date: str, balls_1: str, balls_2: str):
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    circ = int(await count_edition())
    try:
        edition = Edition(circulations=circulations, date=date, balls_1=balls_1, balls_2=balls_2)
        await edition.create()
        logger.info(f'\n{time}   загружен тираж № {circ+1}')
    except UniqueViolationError:
        print('_', end='')


# выбрать все данные
async def select_all_edition():
    # edition_first = await Edition.select('circulations').gino.scalar()  # первая загруженная ячейка по primary_key
    edition_all = await Edition.select('circulations').gino.all()  # выбор всех значений по имени ячейки circulations
    return edition_all


# номер крайнего тиража
# async def last_run():
#     last = await select_all_edition()
#     return int(last[-1][0])


async def count_edition():
    """подсчет количества тиражей"""
    count = await db.func.count(Edition.circulations).gino.scalar()
    return count


# выбрать тираж
async def select_edition(circulations):
    numbers_drawn_1 = await Edition.select('balls_1').where(Edition.circulations == circulations).gino.scalar()
    numbers_drawn_2 = await Edition.select('balls_2').where(Edition.circulations == circulations).gino.scalar()
    date = await Edition.select('date').where(Edition.circulations == circulations).gino.scalar()
    return numbers_drawn_1, numbers_drawn_2, date


# выбрать несколько тиражей поля field (1 or 2)
async def select_field(circulations, field):
    numbers_drawn_1 = await Edition.select(f'balls_{field}').where(Edition.circulations == circulations).gino.scalar()
    return numbers_drawn_1


# поиск выпавших комбинаций в поле 1
async def combination_search_1(comb):
    combination = await Edition.select('circulations').where(Edition.balls_1.like(f'%{comb}%')).gino.all()
    return combination


# поиск выпавших комбинаций в поле 2
async def combination_search_2(comb):
    combination = await Edition.select('circulations').where(Edition.balls_2.like(f'%{comb}%')).gino.all()
    return combination
