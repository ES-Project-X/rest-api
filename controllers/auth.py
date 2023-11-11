from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas as schemas
from crud import user as crud_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # receive user data by body raw json
    return crud_user.create_user(db, user)