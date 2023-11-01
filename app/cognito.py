from fastapi_cognito import CognitoAuth, CognitoSettings
from pydantic_settings import BaseSettings
from pydantic.types import Any

class Settings(BaseSettings):
    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    userpools: dict[str, dict[str, Any]] = {
        "eu": {
            "region": "eu-west-1",
            "userpool_id": "eu-west-1_EQGJijkpw",
            "app_client_id": "2gcaba1b91t1gfnhofgna0g63o"
        }
    }

settings = Settings()

cognito_eu = CognitoAuth(
    settings = CognitoSettings.from_global_settings(settings), userpool_name="eu"
)