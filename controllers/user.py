from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import user as crud_user
from app.database import get_db
import app.schemas as schemas
from app.cognito import get_current_user
from app.models import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("")
async def get_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # receive user id by query params
    return crud_user.get_user(db, current_user.id if current_user is not None else None)

@router.put("/edit")
async def edit_user(user: schemas.UserEdit, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # receive user data by body raw json
    return crud_user.edit_user(db, current_user, user)