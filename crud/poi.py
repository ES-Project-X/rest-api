from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

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