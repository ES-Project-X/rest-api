from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import UploadFile
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

        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename, ExtraArgs={'ACL': 'public-read'})
        key = file.filename

        url = f'''https://{BUCKET_NAME}.s3.amazonaws.com/{urllib.parse.quote(key, safe="~()*!.'")}'''

        return JSONResponse(status_code=200, content={"message": "File Uploaded Successfully", "url": url})

    except Exception as e:
        print("Something Happened: ", e)
        return JSONResponse(status_code=400, content={"message": "Could not upload file"})
