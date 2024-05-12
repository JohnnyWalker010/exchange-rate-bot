from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ExchangeRate(Base):
    """
    Model for storing exchange rates information.

    Attributes:
    - id: unique identifier of the record
    - time: date and time of the record (default is current time)
    - rate: exchange rate value
    """

    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    rate = Column(Float)


engine = create_engine("sqlite:///exchange_rates.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
