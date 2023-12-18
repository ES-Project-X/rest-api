import pytest
from main import app
from app.models import User
from tests.database_test import get_db

def test_get_poi(db: get_db):
    test_user = User(
        email = "example@mail.com",
        username = "example_user",
        cognito_id = "example_cognito_id",
        first_name = "example",
        last_name = "user",
        birth_date = "2000-01-01"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)