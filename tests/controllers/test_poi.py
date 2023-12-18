import pytest
import sys
from fastapi.testclient import TestClient

from tests.database_test import get_test_db
from main import app


client = TestClient(app)

@pytest.fixture
def sample_poi_data():
    return {
        "latitude": 123.456,
        "longitude": 789.012,
        "name": "Test POI",
        "description": "This is a test POI",
        "type": "TestType",
        "picture_url": "https://example.com/test_picture.jpg",
    }

def test_create_poi(sample_poi_data):
    response = client.post("/poi/create", json=sample_poi_data)
    assert response.status_code == 200
    assert "id" in response.json()