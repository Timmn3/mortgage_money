from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import BaseModel


class Statistic(BaseModel):
    __tablename__ = 'statistic'
    circulation = Column(BigInteger, primary_key=True)
    prediction_1 = Column(String(200))
    prediction_2 = Column(String(200))
    coincidence = Column(String(100))

    query: sql.select
