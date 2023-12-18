# tests/test_file.py

from app.schemas import FileUpload
from app.database import Base, get_db
from app.models import User
from sqlalchemy.orm import sessionmaker
from main import app
from datetime import date
from tests.database_test import TestSessionLocal
from unittest.mock import patch
import json
from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
import sys
import os
import boto3
from dotenv import load_dotenv

sys.path.append(".")

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)
REGION_NAME = "eu-west-1"
COGNITO_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USERPOLL_ID")
USERNAME = "kokid46398@rdluxe.com"
PASSWORD = "Sus@naAgui4r"


@pytest.fixture(scope="module", autouse=True)
def load_data():
    db = TestSessionLocal()
    # TODO CLEAR DATABASE
    user = User(id=uuid4(), email="kokid46398@rdluxe.com", username="kokid46398", cognito_id="bffca13b-941f-40e3-ba60-29f620b17266", first_name="Kokid",
                last_name="46398", birth_date=date.today())
    db.commit()
    db.close()


def login():
    # Criar cliente do Cognito
    client = boto3.client('cognito-idp', region_name=REGION_NAME)

    # Obter tokens
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        ClientId=COGNITO_CLIENT_ID,
        AuthParameters={
            "USERNAME": USERNAME,
            "PASSWORD": PASSWORD
        }
    )

    id_token = response['AuthenticationResult']['IdToken']
    if not id_token:
        return None

    return id_token


client = TestClient(app)


def test_upload_to_s3():
    file_upload = {"base64_image": "base64encoding", "image_type": "image/png"}
    token = login()

    response = client.post("/s3/upload", json=file_upload,
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "File Uploaded Successfully" in response.json()["message"]
    assert "image_url" in response.json()