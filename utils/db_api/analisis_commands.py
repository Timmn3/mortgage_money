from asyncpg import UniqueViolationError

from utils.db_api.shemas.admin import AdminBD

# добавление
async def add_analysis(sn: int, amount: int):
    try:
        analysis = AdminBD(sn=sn, amount=amount)
        await analysis.create()
    except UniqueViolationError:
        print(f'количество тиражей для анализа прогноза {amount} не добавленj')

# выбрать количество тиражей для анализа прогноза
async def select_analysis():
    number = await AdminBD.select('amount').where(AdminBD.sn == 1).gino.scalar()
    return number

# измененяем количество тиражей для анализа прогноза
async def change_analysis(amount):
    sn = await AdminBD.query.where(AdminBD.sn == 1).gino.first()
    await sn.update(amount=amount).apply()