from sqlalchemy import Column, BigInteger, String, sql, Float, Integer

from utils.db_api.db_gino import TimedBaseModel


class Users(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    id_proposal = Column(BigInteger)  # номер в БД заявок
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    fio = Column(String(200))  # ФИО
    city = Column(String(100))  # город
    timezone = Column(String(50))  # часовой пояс
    telephone = Column(Integer)  # номер телефона
    referral_id = Column(BigInteger)
    status = Column(String(30))
    balance = Column(Float)
    bill_id = Column(String(200))
    query: sql.select
