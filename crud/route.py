from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

def create_route(db: Session, route: schemas.RouteCreate, added_by: str):
    db_route = models.Route(name=route.name,
                            description=route.description,
                            picture_url=route.picture_url,
                            added_by=added_by)
    try:
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_route

def get_route(db: Session, id: str):
    db_route = db.query(models.Route).filter(models.Route.id == id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

def edit_route(db: Session, route: schemas.RouteEdit):
    db_route = db.query(models.Route).filter(models.Route.id == route.id).first()

    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route.description is not None:
        db_route.description = route.description

    if route.picture_url is not None:
        db_route.picture_url = route.picture_url

    try:
        db.commit()
        db.refresh(db_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_route

def remove_route(db: Session, id: str):
    db_route = db.query(models.Route).filter(models.Route.id == id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(db_route)
    db.commit()
    return db_route