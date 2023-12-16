from email.mime import image
from aiohttp import FormData
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import boto3
from dotenv import load_dotenv
import os
import urllib.parse
import base64
from io import BytesIO
import app.schemas as schemas
import uuid

load_dotenv(".env")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


async def upload_to_s3(file: schemas.FileUpload, current_user: str, db: Session):

    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        
        image_type = file.image_type.split("/")[1]

        # Generate random UUID for the file name
        unique_id = uuid.uuid4()
        # Convert UUID format to hex string
        file_name = str(unique_id).replace("-", "") + "." + image_type

        print(file_name)
        print(file.base64_image)

        image_data = base64.b64decode(file.base64_image)
        image_file = BytesIO(image_data)

        s3.upload_fileobj(image_file, BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'})
        

        url = f'''https://{BUCKET_NAME}.s3.amazonaws.com/{urllib.parse.quote(file_name, safe="~()*!.'")}'''

        return JSONResponse(status_code=200, content={"message": "File Uploaded Successfully", "image_url": url})

    except Exception as e:
        print("Something Happened: ", e)
        return JSONResponse(status_code=400, content={"message": "Could not upload file"})