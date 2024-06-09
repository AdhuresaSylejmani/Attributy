from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessedData(Base):
    """
    A class used to represent the processed data table in a database.

    Attributes
    ----------
    id : int
        Primary key, autoincremented ID of the record.
    ip_address : str
        IP address of the user.
    marketing_channel : str
        Marketing channel through which the user was acquired.
    purchase : float
        Purchase amount made by the user.
    state : str
        State where the user is located.
    time_spent_seconds : int
        Time spent by the user on the site in seconds.
    converted : int
        Indicates if the user made a purchase (1 if true, 0 if false).
    state_abbreviation : str
        Abbreviation of the state where the user is located.
    purchase_normalized : float
        Normalized purchase amount.
    percentile_85_state : int
        Indicates if the user's purchase is in the 85th percentile within their state (1 if true, 0 if false).
    percentile_85_national : int
        Indicates if the user's purchase is in the 85th percentile nationally (1 if true, 0 if false).
    """

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
