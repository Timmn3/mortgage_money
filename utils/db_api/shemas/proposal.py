from sqlalchemy import Column, String, sql, Integer, BigInteger

from utils.db_api.db_gino import TimedBaseModel


class Proposal(TimedBaseModel):
    __tablename__ = 'proposal'
    id = Column(Integer, primary_key=True, autoincrement=True)  # автоинкрементируемый
    user_id = Column(BigInteger)
    fio = Column(String(100))
    variant_proposal = Column(String(200))  # вариант заявки
    status_proposal = Column(String(100))  # статус заявки
    approved_amount = Column(BigInteger)  # одобренная сумма
    loan_amount = Column(BigInteger)  # величина взятого займа
    photo_passport_1 = Column(String(200))
    photo_passport_2 = Column(String(200))
    photo_snils = Column(String(200))
    photo_from_1_credit_history_site = Column(String(2000))
    photo_from_2_credit_history_site = Column(String(2000))

    query: sql.select
