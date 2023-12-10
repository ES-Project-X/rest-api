from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cognito import CognitoToken
from app.database import engine
from app.cognito import cognito_eu
from controllers import auth, user, poi, route, file
import os

import app.models as models

app = FastAPI(
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

models.Base.metadata.create_all(bind=engine)

origins = os.environ.get("FRONTEND_URL").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(poi.router)
app.include_router(route.router)
app.include_router(file.router)

@app.get("/")
async def root():
    return {"message": "Sup N*ggas"}

@app.get("/test-cognito-auth")
async def test_cognito_auth(token: CognitoToken = Depends(cognito_eu.auth_required)):
    """
    Notas:
    - Basta colocar o argumento "token" desta forma para que seja verificada a autenticação.
    - No cognito.py está a configuração do "cognito_eu", que é importado e usado aqui.
    - Passar o JWT token (access_token) no header "Authorization" com o prefixo "Bearer " (Authorization: Bearer <access_token>).
    - Conteúdo do token:
    {
        "origin_jti": null,
        "sub": "1cfd853e-f2e8-4db9-9b3c-5b20070e2dd9",
        "event_id": "ee5fed89-4b6d-4e9c-9fd9-0a549aa88395",
        "token_use": "access",
        "scope": "openid email",
        "auth_time": 1698877020,
        "iss": "https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_EQGJijkpw",
        "exp": 1698880620,
        "iat": 1698877020,
        "jti": "6b6d8b93-b2b8-4d4c-965a-28732fd44ebb",
        "client_id": "2gcaba1b91t1gfnhofgna0g63o",
        "username": "1cfd853e-f2e8-4db9-9b3c-5b20070e2dd9"
    }
    - "username" é a referência para o utilizador no Cognito (possui email, family_name e given_name).
    """
    return token
