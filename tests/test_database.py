import os
import sys
src_path = "/Users/adhuresasylejmani/Desktop/bb/Attributy"
sys.path.append(src_path)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import DatabaseConnection
from src.models import Base

DATABASE_URL = os.getenv("DATABASE_TEST_URL", "sqlite:///./test.db")

@pytest.fixture(scope='module')
def db():
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = DatabaseConnection(DATABASE_URL)
    db.connect()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_add_row(db):
    data = {
        'ip_address': '192.168.1.1',
        'marketing_channel': 'A',
        'purchase': 100.0,
        'state': 'NY',
        'time_spent_seconds': 120,
        'converted': 1,
        'state_abbreviation': 'NY',
        'purchase_normalized': 0.5,
        'percentile_85_state': 1,
        'percentile_85_national': 0
    }
    db.add_row('processed_data', data)
    result = db.fetch_data('SELECT * FROM processed_data WHERE ip_address="192.168.1.1"')
    assert result is not None
    assert result[0]['ip_address'] == '192.168.1.1'
