from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas as schemas
from crud import user as crud_user
from app.database import get_db
from app.cognito import get_cognito_username

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db), cognito_username: str = Depends(get_cognito_username)):
    return crud_user.create_user(db, user, cognito_username)