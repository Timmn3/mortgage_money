from sqlalchemy import Column, BigInteger, String, sql, Integer

from utils.db_api.db_gino import TimedBaseModel


class Users(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    id_proposal = Column(String(200))  # номера в БД заявок
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    fio = Column(String(200))  # ФИО
    city = Column(String(100))  # город
    timezone = Column(Integer)  # часовой пояс
    telephone = Column(BigInteger)  # номер телефона
    referral_id = Column(String(100))  # реферальная ссылка
    my_referrals = Column(String(10000))  # список пользователей зарегистрированных по реферальной ссылке
    bonus_1 = Column(Integer)
    bonus_2 = Column(Integer)
    money = Column(BigInteger)  # сумма денег
    role = Column(String(50))  # админ, обработчик заявок, менеджер, копирайтер, клиент
    balance = Column(Integer)
    status = Column(String(50))

    query: sql.select

