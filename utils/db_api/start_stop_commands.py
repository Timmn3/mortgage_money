from asyncpg import UniqueViolationError

from utils.db_api.shemas.start_stop import Start_stop


# добавление
async def add_start_stop(sn: int, boolean: str):
    try:
        start_stop = Start_stop(sn=sn, bool=bool)
        await start_stop.create()
    except UniqueViolationError:
        print(f'add_start_stop не добавлен')

# получить значение
async def select_start_stop():
    boolean = await Start_stop.select('bool').where(Start_stop.sn == 1).gino.scalar()
    return boolean

# измененяем значение
async def change_start_stop(boolean):
    sn = await Start_stop.query.where(Start_stop.sn == 1).gino.first()
    await sn.update(bool=boolean).apply()