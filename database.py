from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from constants import TABLE_NAME, DB_FILE_PATH

Base = declarative_base()


class ExchangeRate(Base):
    """
    Model for storing exchange rates information.

    Attributes:
    - id: unique identifier of the record
    - time: date and time of the record (default is current time)
    - rate: exchange rate value
    """

    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    rate = Column(Float)


engine = create_engine(f"sqlite:///{DB_FILE_PATH}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
