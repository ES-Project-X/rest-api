from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import route as route_crud
from app.database import get_db
import app.schemas as schemas
from app.cognito import get_current_user
from app.models import User

router = APIRouter(prefix="/route", tags=["route"])

@router.post("/create")
async def create_route(route: schemas.RouteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return route_crud.create_route(db=db, route=route, added_by=current_user.id)

@router.get("/get")
async def get_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return route_crud.get_routes_by_user(db=db, user_id=current_user.id)

@router.delete("/delete/{id}")
async def delete_route(id : str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return route_crud.delete_route(db=db, id=id)