from fastapi.testclient import TestClient
import uuid
import pytest
from app.models import Base, User, POI
from app.database import SessionLocal, engine
from main import app
from unittest.mock import patch

client = TestClient(app)


@pytest.fixture(scope="session")
def setup_db():
    try:
        # Create the test database
        Base.metadata.create_all(bind=engine)
        # Run the tests
        yield
    finally:
        # Drop the test database
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def create_test_user(db_session):
    # Create a real user object in the test database
    id_user = str(uuid.uuid4())
    user = User(
        id=id_user,
        username="test_user",
        email="test@example.com",
        cognito_id="test_cognito_id",

    )
    db_session.add(user)
    db_session.commit()
    return id_user

@pytest.fixture
def mock_user(create_test_user):
    # Use the real user object from the fixture and return its ID
    return create_test_user


@pytest.fixture
def create_test_poi(db_session, mock_user):
    print("\n\n\nCreating test POI")
    # Create a sample POI with a valid UUID for added_by
    poi = POI(
        id=str(uuid.uuid4()),  # Generate a valid UUID string for ID
        name="Test POI",
        description="Test Description",
        type="Test Type",
        added_by=mock_user.id,  # Assign the ID of the mock user
        picture_url="https://example.com/image.jpg",
        rating_positive=5,
        rating_negative=1,
        latitude=40.7128,
        longitude=-74.0060
    )
    # Add the POI to the database session
    db_session.add(poi)
    db_session.commit()
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