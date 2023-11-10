from sqlalchemy import Column, String, sql, Float

from utils.db_api.db_gino import TimedBaseModel


class Edition(TimedBaseModel):
    __tablename__ = 'edition'
    circulations = Column(String(10), primary_key=True)
    date = Column(String(20))
    balls_1 = Column(String(20))
    balls_2 = Column(String(20))

    query: sql.select
