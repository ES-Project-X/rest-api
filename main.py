from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import app.models as models, app.schemas as schemas, app.crud as crud
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session

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

@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # receive user data by body raw json
    return crud.create_user(db, user)

@app.get("/profile")
async def get_user(id: str, db: Session = Depends(get_db)):
    # receive user id by query params
    return crud.get_user(db, id)

@app.put("/edit_profile")
async def edit_user(id: str, user: schemas.UserEdit, db: Session = Depends(get_db)):
    # receive user id by query params
    # receive user data by body raw json
    return crud.edit_user(db, id, user)

@app.get("/pois")
async def get_poi(coords: list[float] = None, type: list[str] = Query(None), name: str = None, db: Session = Depends(get_db)):
    # receive coordinates by query params
    # receive type by query params
    # receive name by query params
    return crud.filter_pois(db, coords, type, name)

