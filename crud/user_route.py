from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

def create_user_route(db: Session, id: str, user_route: schemas.UserRouteManage):
    db_user_route = models.UserRoute(user_id=id,
                                     route_id=user_route.route_id,
                                     rating=user_route.rating)
    try:
        db.add(db_user_route)
        db.commit()
        db.refresh(db_user_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_route

def get_user_route(db: Session, id: str, user_route: schemas.UserRouteBase):
    db_user_route = db.query(models.UserRoute).filter(models.UserRoute.user_id == id, models.UserRoute.route_id == user_route.route_id).first()
    if db_user_route is None:
        raise HTTPException(status_code=404, detail="User Route not found")
    return db_user_route

def update_user_route(db: Session, id: str, user_route: schemas.UserRouteManage):
    db_user_route = db.query(models.UserRoute).filter(models.UserRoute.user_id == id, models.UserRoute.route_id == user_route.route_id).first()

    if db_user_route is None:
        raise HTTPException(status_code=404, detail="User Route not found")
    
    if user_route.rating is not None:
        if db_user_route.rating is None:
            db_user_route.rating = user_route.rating

            db_route = db.query(models.Route).filter(models.Route.id == user_route.route_id).first()
            if user_route.rating:
                db_route.rating_positive += 1
            else:
                db_route.rating_negative += 1

        elif db_user_route.rating != user_route.rating:
            db_user_route.rating = user_route.rating

            db_route = db.query(models.Route).filter(models.Route.id == user_route.route_id).first()
            if user_route.rating:
                db_route.rating_positive += 1
                db_route.rating_negative -= 1
            else:
                db_route.rating_negative += 1
                db_route.rating_positive -= 1

    try:
        db.commit()
        db.refresh(db_user_route)
        db.refresh(db_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_route

def remove_user_route(db: Session, id: str, user_route: schemas.UserRouteBase):
    db_user_route = db.query(models.UserRoute).filter(models.UserRoute.user_id == id, models.UserRoute.route_id == user_route.route_id).first()
    if db_user_route is None:
        raise HTTPException(status_code=404, detail="User Route not found")
    
    if db_user_route.rating is not None:
        db_route = db.query(models.Route).filter(models.Route.id == user_route.route_id).first()
        if db_user_route.rating:
            db_route.rating_positive -= 1
        else:
            db_route.rating_negative -= 1

    try:
        db.delete(db_user_route)
        db.commit()
        db.refresh(db_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_route