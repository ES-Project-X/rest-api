from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from crud import file as crud_file
from app.database import get_db
from app.cognito import get_current_user
from app.models import User
import app.schemas as schemas

router = APIRouter(prefix="/s3", tags=["Upload to S3"])


@router.post("/upload")
async def upload_to_s3(image: schemas.FileUpload, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # receive poi data by body raw json
    return await crud_file.upload_to_s3(image, current_user.id, db)