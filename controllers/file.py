from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from crud import file as crud_file
from app.database import get_db
import app.schemas as schemas
from app.cognito import get_current_user
from app.models import User

router = APIRouter(prefix="/s3", tags=["Upload to S3"])

@router.post("/upload")
async def upload_to_s3(file: UploadFile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_file.upload_to_s3(file, db, current_user.id)
    