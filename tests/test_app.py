from fastapi.testclient import TestClient
import sys

import pytest
''' sys.path.append("..")
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sup N*ggas"}
 '''

from app.models import POI

# ModuleNotFoundError: No module named 'database_test' ???

from tests.database_test import get_test_db


@pytest.fixture
def create_test_poi():

    # Get a test database
    db = get_test_db()

    # Create a sample POI
    poi = POI(
        id="1",  # Replace with an actual UUID
        name="Test POI",
        description="Test Description",
        type="Test Type",
        added_by="1",
        picture_url="https://example.com/image.jpg",
        rating_positive=5,
        rating_negative=1
    )
    # Add the POI to the database
    db.add(poi)
    db.commit()
    db.refresh(poi)
    return poi


def test_get_poi_by_id(create_test_poi, client):
    # Get the ID of the created POI
    poi_id = create_test_poi.poi.id

    # Make a request to the endpoint with the POI ID
    response = client.get(f"/id/{poi_id}")

    # Assert the response status code and content
    assert response.status_code == 200

    # You might want to validate the response content further based on your endpoint's expected output
    # For instance, you could assert specific attributes of the POI returned by the endpoint
    returned_poi = response.json()
    assert returned_poi["name"] == "Test POI"
    assert returned_poi["description"] == "Test Description"
    # Add more assertions based on your POI attributes