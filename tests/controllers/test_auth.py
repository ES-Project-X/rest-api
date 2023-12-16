''' from fastapi.testclient import TestClient
from main import app
from database_test import TestingSessionLocal
import pytest

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def load_data():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_register():

    user_data = {
        "email": "test@example.com",
        "username": "test",
        "cognito_username": "test",
        "first_name": "Test",
        "last_name": "Test",
        "birth_date": "2020-01-01",
    }
    
    response = client.post("/auth/register", json=user_data)
    created_user = response.json()
    print("Aqui:", created_user)
    assert response.status_code == 200
    assert created_user["email"] == user_data["email"]
 '''