from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import BaseModel


class Start_stop(BaseModel):
    __tablename__ = 'start_stop'
    sn = Column(BigInteger, primary_key=True)
    bool = Column(String)

    query: sql.select
