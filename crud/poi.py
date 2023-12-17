from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException
from datetime import date, datetime, timedelta

XP_POS_RATING_RECEIVED=50
XP_POS_RATING_GIVEN=10
XP_STATUS_GIVEN=50
XP_STATUS_RECEIVED=5
XP_CREATED_POI=50

def remove_all(db: Session):
    db.query(models.Status).delete()
    db.query(models.UserPOI).delete()
    db.query(models.POI).delete()
    db.commit()
    return {"msg": "All POIs removed"}

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

    db_user_poi = models.UserPOI(user_id=added_by, poi_id=db_poi.id, rating=True)
    db_user = db.query(models.User).filter(models.User.id == added_by).first()
    db_user.added_pois_count += 1
    db_user.total_xp += XP_CREATED_POI
    try:
        db.add(db_user_poi)
        db.commit()
        db.refresh(db_user_poi)
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": db_poi.id,
        "latitude": db_poi.latitude,
        "longitude": db_poi.longitude,
        "name": db_poi.name,
        "description": db_poi.description,
        "type": db_poi.type,
        "added_by": db_poi.added_by,
        "picture_url": db_poi.picture_url,
        "rating_positive": db_poi.rating_positive,
        "rating_negative": db_poi.rating_negative,
    }

def get_poi(db: Session, poi_id: str, user_id: str = None):
    db_poi = db.query(models.POI).filter(models.POI.id == poi_id).first()
    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    # check if user rated this poi and add this info to response
    db_user_poi = None
    if user_id is not None:
        db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == user_id, models.UserPOI.poi_id == poi_id).first()
    rate = None
    status = False
    if db_user_poi is not None:
        rate = db_user_poi.rating
        if db_user_poi.last_status_given and db_user_poi.last_status_given == date.today():
            status = True

    return {
        "id": db_poi.id,
        "latitude": db_poi.latitude,
        "longitude": db_poi.longitude,
        "name": db_poi.name,
        "description": db_poi.description,
        "type": db_poi.type,
        "added_by": db_poi.added_by,
        "picture_url": db_poi.picture_url,
        "rating_positive": db_poi.rating_positive,
        "rating_negative": db_poi.rating_negative,
        "rate": rate,
        "status": status,
    }


def get_pois_by_cluster(db: Session, clusters: list[list[float]]):
    # receive in format [max_lat, min_lat, max_long, min_long]

    if clusters is None:
        return db.query(models.POI).all()
    
    db_pois = []
    
    for cluster in clusters:
        if len(cluster) != 4:
            raise HTTPException(status_code=400, detail="Invalid cluster format")
        
        if cluster[0] < cluster[1] or cluster[2] < cluster[3]:
            raise HTTPException(status_code=400, detail="Invalid cluster format")
        
        if cluster[0] > 90 or cluster[0] < -90 or cluster[1] > 90 or cluster[1] < -90:
            raise HTTPException(status_code=400, detail="Invalid cluster format")
        
        if cluster[2] > 180 or cluster[2] < -180 or cluster[3] > 180 or cluster[3] < -180:
            raise HTTPException(status_code=400, detail="Invalid cluster format")
        
        db_pois += db.query(models.POI).filter(models.POI.latitude <= cluster[0],
                                               models.POI.latitude >= cluster[1],
                                               models.POI.longitude <= cluster[2],
                                               models.POI.longitude >= cluster[3]).all()
        
    return db_pois

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

def rate_poi_existence(db: Session, id: str, rating: bool, user_id: str):
    db_poi = db.query(models.POI).filter(models.POI.id == id).first()
    if db_poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    
    db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == user_id, models.UserPOI.poi_id == id).first()
    time = 0
    if db_user_poi is not None:
        if not db_user_poi.existence_cooldown:
            return {"time": -1}
        if datetime.now() - db_user_poi.existence_cooldown < timedelta(hours=72):
            time = 72*3600 - (datetime.now() - db_user_poi.existence_cooldown).seconds
        else:
            if rating != db_user_poi.rating:
                db_user_poi.rating = rating
                db_user_poi.existence_cooldown = datetime.now()
                if rating:
                    db_poi.rating_positive += 1
                    db_poi.rating_negative -= 1
                else:
                    db_poi.rating_positive -= 1
                    db_poi.rating_negative += 1

    else:
        db_user_poi = models.UserPOI(user_id=user_id, poi_id=id, rating=rating, existence_cooldown=datetime.now())
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if rating:
            db_poi.rating_positive += 1
        else:
            db_poi.rating_negative += 1
        
        db_poi_addedby = db.query(models.User).filter(models.User.id == db_poi.added_by).first()
        
        if user_id != db_poi.added_by:
            db_user.given_ratings_count += 1                        
            db_poi_addedby.received_ratings_count += 1

            if rating:
                db_user.total_xp += XP_POS_RATING_GIVEN 
                db_poi_addedby.total_xp += XP_POS_RATING_RECEIVED
    


        db.add(db_user_poi)
        db.commit()
        db.refresh(db_user)
        db.refresh(db_poi_addedby)

    db.commit()
    db.refresh(db_poi)
    db.refresh(db_user_poi)

    return {"time": time}

def get_poi_status(db: Session, id: str):
    today = db.query(models.Status).filter(models.Status.poi_id == id, models.Status.date == date.today()).first()
    yesterday = db.query(models.Status).filter(models.Status.poi_id == id, models.Status.date == date.today() - timedelta(days=1)).first()
    seven_days = db.query(models.Status).filter(models.Status.poi_id == id, models.Status.date >= date.today() - timedelta(days=7)).all()
    thirty_days = db.query(models.Status).filter(models.Status.poi_id == id, models.Status.date >= date.today() - timedelta(days=30)).all()
    all_time = db.query(models.Status).filter(models.Status.poi_id == id).all()

    return {
        "today": today.balance if today else 0,
        "yesterday": yesterday.balance if yesterday else 0,
        "7_days": sum([status.balance for status in seven_days]),
        "1_month": sum([status.balance for status in thirty_days]),
        "all_time": sum([status.balance for status in all_time])
    }

def rate_poi_status(db: Session, id: str, rating: bool, user_id: str):
    db_poi = db.query(models.Status).filter(models.Status.poi_id == id, models.Status.date == date.today()).first()
    db_user_poi = db.query(models.UserPOI).filter(models.UserPOI.user_id == user_id, models.UserPOI.poi_id == id).first()

    if db_poi is None:
        # create new status for this poi
        db_poi = models.Status(poi_id=id)
        db.add(db_poi)
        db.commit()
        db.refresh(db_poi)
    
    elif db_user_poi and db_user_poi.last_status_given == date.today():
        raise HTTPException(status_code=404, detail="POI Status already rated today") #TODO alterar código do erro, não tenho net para ver qual é

    if rating:
        db_poi.balance += 1
    else:
        db_poi.balance -= 1


    db_poi_addedby = db.query(models.POI).filter(models.POI.id == id).first()

    if user_id != db_poi_addedby.added_by:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        db_user.total_xp += XP_STATUS_GIVEN
        db_poi_user_added = db.query(models.User).filter(models.User.id == db_poi_addedby.added_by).first()
        db_poi_user_added.total_xp += XP_STATUS_RECEIVED

    db_user_poi.last_status_given = date.today()

    db.commit()
    db.refresh(db_poi)
    db.refresh(db_user_poi)

    return db_poi