from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import user as crud_user
from app.database import get_db
import app.schemas as schemas

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{id}}")
async def get_user(id: str, db: Session = Depends(get_db)):
    # receive user id by query params
    return crud_user.get_user(db, id)

@router.put("/edit/{id}")
async def edit_user(id: str, user: schemas.UserEdit, db: Session = Depends(get_db)):
    # receive user id by query params
    # receive user data by body raw json
    return crud_user.edit_user(db, id, user)