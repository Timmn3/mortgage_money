from sqlalchemy import Column, String, sql, Integer

from utils.db_api.db_gino import BaseModel


class AdminBD(BaseModel):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)  # автоинкрементируемый
    greeting_text = Column(String(500))  # текст приветствия
    greeting_video = Column(String(500))  # видео приветствия по id
    greeting_photo = Column(String(500))  # фото приветствия по id
    documents_id = Column(String(1000))  # список id документов лоя ознакомления
    channel_list = Column(String(500))  # список каналов
    chat_ids_list = Column(String(500))  # список чат id каналов
    technical_support = Column(String(100))  # техническая поддержка
    tariff = Column(Integer)  # тариф
    set_bonus_1 = Column(Integer)  # установить бонус 1
    set_bonus_2 = Column(Integer)  # установить бонус 2
    variants_proposal = Column(String(500))  # варианты заявок
    variants_reason_rejection = Column(String(500))  # варианты причин отклонения
    newsletter_text = Column(String(500))  # текст рассылки
    newsletter_period = Column(Integer)  # период рассылки
    newsletter_whom = Column(String(500))  # кому отправлять

    query: sql.select
