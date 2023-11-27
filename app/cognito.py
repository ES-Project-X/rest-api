from fastapi_cognito import CognitoAuth, CognitoSettings, CognitoToken
from fastapi import Depends
from pydantic_settings import BaseSettings
from pydantic.types import Any
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
import os

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

userpool_id = str(os.environ.get("COGNITO_USERPOLL_ID"))
app_client_id = str(os.environ.get("COGNITO_APP_CLIENT_ID"))
class Settings(BaseSettings):
    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    userpools: dict[str, dict[str, Any]] = {
        "eu": {
            "region": "eu-west-1",
            "userpool_id": userpool_id,
            "app_client_id": app_client_id,
        }
    }

settings = Settings()

cognito_eu = CognitoAuth(
    settings = CognitoSettings.from_global_settings(settings), userpool_name="eu"
)
    
def get_current_user(token: CognitoToken = Depends(cognito_eu.auth_required), db: Session = Depends(get_db)) -> str:
    return db.query(models.User).filter(models.User.cognito_username == token.username).first().id

def get_cognito_username(token: CognitoToken = Depends(cognito_eu.auth_required)) -> str:
    return token.username