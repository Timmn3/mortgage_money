from sqlalchemy import Column, String, sql, Integer

from utils.db_api.db_gino import BaseModel


class AdminBD(BaseModel):
    __tablename__ = 'admin'
    sn = Column(Integer, primary_key=True)
    greeting_text = Column(String(400))  # текст приветствия
    channel_list = Column(String(200))  # список каналов
    technical_support = Column(String(100))  # техническая поддержка
    tariff = Column(String(50))  # тариф
    variants_proposal = Column(String(200))  # варианты заявок
    variants_reason_rejection = Column(String(200))  # варианты причин отклонения

    query: sql.select
