from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException
from uuid import uuid4

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email,
                          password=user.password,
                          username=user.username,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          birth_date=user.birth_date)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user

def get_user(db: Session, id: str):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def edit_user(db: Session, id: str, user: schemas.UserEdit):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email is not None:
        if user.email == db_user.email:
            raise HTTPException(status_code=400, detail="Email is the same")
        
        db_test = db.query(models.User).filter(models.User.email == user.email).first()
        if db_test is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user.email = user.email

    if user.username is not None:
        if user.username == db_user.username:
            raise HTTPException(status_code=400, detail="Username is the same")
        
        db_test = db.query(models.User).filter(models.User.username == user.username).first()
        if db_test is not None:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        db_user.username = user.username

    if user.password is not None:
        db_user.password = user.password

    if user.first_name is not None:
        db_user.first_name = user.first_name

    if user.last_name is not None:
        db_user.last_name = user.last_name

    if user.image_url is not None:
        db_user.image_url = user.image_url

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user

# remove method shouldn't be literally deleting the user from the database, just set the user's status to inactive
def remove_user():
    pass

def create_poi(db: Session, poi: schemas.POICreate, added_by: str):
    db_poi = models.POI(latitude=poi.latitude,
                        longitude=poi.longitude,
                        name=poi.name,
                        description=poi.description,
                        type=poi.type,
                        added_by=added_by,
                        picture_url=poi.picture_url)
    try:
        db.add(db_poi)
        db.commit()
        db.refresh(db_poi)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_poi

def get_poi(db: Session, id: str):
    db_poi = db.query(models.POI).filter(models.POI.id == id).first()
    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    return db_poi

def edit_poi(db: Session, poi: schemas.POIEdit):
    db_poi = db.query(models.POI).filter(models.POI.id == poi.id).first()

    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    
    if poi.description is not None:
        db_poi.description = poi.description

    if poi.picture_url is not None:
        db_poi.picture_url = poi.picture_url

    try:
        db.commit()
        db.refresh(db_poi)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_poi

def remove_poi(db: Session, id: str):
    db_poi = db.query(models.POI).filter(models.POI.id == id).first()
    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    db.delete(db_poi)
    db.commit()
    return db_poi

def create_user_poi(db: Session, id: str, user_poi: schemas.UserPOIManage):
    db_user_poi = models.UserPOI(user_id=id,
                                 poi_id=user_poi.poi_id,
                                 rating=user_poi.rating)
    try:
        db.add(db_user_poi)
        db.commit()
        db.refresh(db_user_poi)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_poi

def get_user_poi(db: Session, id: str, user_poi: schemas.UserPOIBase):
    db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == id, models.UserPOI.poi_id == user_poi.poi_id).first()
    if db_user_poi is None:
        raise HTTPException(status_code=404, detail="User POI not found")
    return db_user_poi

def update_user_poi(db: Session, id: str, user_poi: schemas.UserPOIManage):
    db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == id, models.UserPOI.poi_id == user_poi.poi_id).first()

    if db_user_poi is None:
        raise HTTPException(status_code=404, detail="User POI not found")
    
    if user_poi.rating is not None:
        if db_user_poi.rating is None:
            db_user_poi.rating = user_poi.rating

            db_poi = db.query(models.POI).filter(models.POI.id == user_poi.poi_id).first()
            if user_poi.rating:
                db_poi.rating_positive += 1
            else:
                db_poi.rating_negative += 1

        elif db_user_poi.rating != user_poi.rating:
            db_user_poi.rating = user_poi.rating

            db_poi = db.query(models.POI).filter(models.POI.id == user_poi.poi_id).first()
            if user_poi.rating:
                db_poi.rating_positive += 1
                db_poi.rating_negative -= 1
            else:
                db_poi.rating_negative += 1
                db_poi.rating_positive -= 1

    try:
        db.commit()
        db.refresh(db_user_poi)
        db.refresh(db_poi)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_poi

def remove_user_poi(db: Session, id: str, user_poi: schemas.UserPOIBase):
    db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == id, models.UserPOI.poi_id == user_poi.poi_id).first()
    if db_user_poi is None:
        raise HTTPException(status_code=404, detail="User POI not found")
    
    if db_user_poi.rating is not None:
        db_poi = db.query(models.POI).filter(models.POI.id == user_poi.poi_id).first()
        if db_user_poi.rating:
            db_poi.rating_positive -= 1
        else:
            db_poi.rating_negative -= 1

    try:
        db.delete(db_user_poi)
        db.commit()
        db.refresh(db_poi)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user_poi

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