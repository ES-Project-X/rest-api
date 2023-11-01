from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cognito import CognitoToken

from sqlalchemy.orm import Session

import app.models as models, app.schemas as schemas, app.crud as crud
from app.database import SessionLocal, engine
from app.cognito import cognito_eu

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # receive user data by body raw json
    return crud.create_user(db, user)

@app.get("/user/{id}}")
async def get_user(id: str, db: Session = Depends(get_db)):
    # receive user id by query params
    return crud.get_user(db, id)

@app.put("/user/edit/{id}")
async def edit_user(id: str, user: schemas.UserEdit, db: Session = Depends(get_db)):
    # receive user id by query params
    # receive user data by body raw json
    return crud.edit_user(db, id, user)

@app.get("/poi/{id}")
async def get_poi(id: str, db: Session = Depends(get_db)):
    # receive poi id by query params
    return crud.get_poi(db, id)

@app.get("/pois")
async def get_pois(max_lat: list[float] = Query(None), min_lat: list[float] = Query(None), max_lng: list[float] = Query(None), min_lng: list[float] = Query(None), db: Session = Depends(get_db)):
    # receive cluster by query params
    clusters = []
    if max_lat is None or min_lat is None or max_lng is None or min_lng is None:
        raise HTTPException(status_code=400, detail="Invalid cluster format")
    if len(max_lat) != len(min_lat) or len(max_lat) != len(max_lng) or len(max_lat) != len(min_lng):
        raise HTTPException(status_code=400, detail="Invalid cluster format")
    for i in range(len(max_lat)):
        clusters.append([max_lat[i], min_lat[i], max_lng[i], min_lng[i]])

    return crud.get_pois_by_cluster(db, clusters)

