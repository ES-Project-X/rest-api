from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException, UploadFile
import boto3
from dotenv import load_dotenv
import os
import urllib.parse


load_dotenv(".env")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


async def upload_to_s3(file: UploadFile, db: Session, user_id: int):
    
    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:

        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)

        key = file.filename

        url = f'''https://{BUCKET_NAME}.s3.amazonaws.com/{urllib.parse.quote(key, safe="~()*!.'")}'''

        return url

    except Exception as e:
        print("Something Happened: ", e)
        return e


    
    

