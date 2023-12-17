# tests/test_file.py
from http import client
import json
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
import sys
from main import app
from sqlalchemy.orm import sessionmaker
from app.models import User

from app.database import Base, get_db
from app.schemas import  FileUpload


@pytest.fixture
def mock_get_current_user(monkeypatch):
    def mock_get_current_user():
        return User(id=1, username="testuser", email="test@example.com")
    monkeypatch.setattr("app.cognito.get_current_user", mock_get_current_user)

@pytest.mark.asyncio
async def test_upload_to_s3(mock_get_current_user):
    client = TestClient(app)
    
    file_upload ={ "base64_image": "base64encoding", "image_type": "image/png" }

    response = client.post("/s3/upload", json=file_upload)

    assert response.status_code == 200
    assert "File Uploaded Successfully" in response.json()["message"]
    assert "image_url" in response.json()