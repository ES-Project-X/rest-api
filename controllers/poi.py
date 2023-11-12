from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import poi as crud_poi
from app.database import get_db
from fastapi import Query, HTTPException
import app.schemas as schemas
from app.cognito import get_current_user
from typing import Optional

router = APIRouter(prefix="/poi", tags=["poi"])

@router.get("/{id}/")
async def get_poi(id: str, current_user: Optional[str] = Depends(get_current_user), db: Session = Depends(get_db)):
    # receive poi id by query params
    return crud_poi.get_poi(db, id, current_user)

@router.get("/cluster")
async def get_pois(max_lat: list[float] = Query(None), min_lat: list[float] = Query(None), max_lng: list[float] = Query(None), min_lng: list[float] = Query(None), db: Session = Depends(get_db)):
    # receive cluster by query params
    clusters = []
    if max_lat is None or min_lat is None or max_lng is None or min_lng is None:
        raise HTTPException(status_code=400, detail="Invalid cluster format")
    if len(max_lat) != len(min_lat) or len(max_lat) != len(max_lng) or len(max_lat) != len(min_lng):
        raise HTTPException(status_code=400, detail="Invalid cluster format")
    for i in range(len(max_lat)):
        clusters.append([max_lat[i], min_lat[i], max_lng[i], min_lng[i]])

    return crud_poi.get_pois_by_cluster(db, clusters)

@router.put("/exists")
async def rate_poi_existence(poi: schemas.POIRateExistence, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # receive poi id and rating by body raw json
    return crud_poi.rate_poi_existence(db, poi.id, poi.rating, current_user)