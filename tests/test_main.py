from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Sup N*ggas"}

def test_read_register():
    response = client.post("/register", json={"email": "testuser@mail.com", "username": "testuser", "password": "password", "first_name": "test", "last_name": "user", "birth_date": "01/01/2000"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
