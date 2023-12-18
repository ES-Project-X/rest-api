from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

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