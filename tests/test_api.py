import pytest

import sys
src_path = "/Users/adhuresasylejmani/Desktop/bb/Attributy/src"
sys.path.append(src_path)

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_redirect_to_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Go to /docs for API documentation"}

def test_process_data():
    response = client.post(
        "/process_data/",
        json={
            "data": [
                {
                    "ip_address": "192.168.1.1",
                    "marketing_channel": "A",
                    "purchase": 100.0,
                    "state": "NY",
                    "time_spent_seconds": 120,
                    "converted": 1,
                    "state_abbreviation": "NY",
                    "purchase_normalized": 0.5,
                    "percentile_85_state": 1,
                    "percentile_85_national": 0
                }
            ]
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Data processed and stored successfully"}

def test_get_data():
    response = client.get("/data/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
