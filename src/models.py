from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessedData(Base):
    __tablename__ = 'processed_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(15))
    marketing_channel = Column(String(50))  
    purchase = Column(Float)
    state = Column(String(50))
    time_spent_seconds = Column(Integer)
    converted = Column(Integer)
    state_abbreviation = Column(String(50))
    purchase_normalized = Column(Float)
    percentile_85_state = Column(Integer)
    percentile_85_national = Column(Integer)
