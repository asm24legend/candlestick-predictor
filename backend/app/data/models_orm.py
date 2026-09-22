from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class OHLCV(Base):
    __tablename__ = "ohlcv"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)