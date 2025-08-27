########## Modules ##########
import boto3

from pathlib import Path

from fastapi import UploadFile

from core.config import settings

########## Variables ##########
bucket_name = settings.WASABI_BUCKET_NAME

########## WASABI ##########
s3 = boto3.client('s3',
    endpoint_url="https://s3.us-central-1.wasabisys.com",
    region_name="us-central-1",
    aws_access_key_id=settings.WASABI_ACCESS_KEY,
    aws_secret_access_key=settings.WASABI_SECRET_KEY,
)

########## Upload Function ##########
async def upload_original_video(video_id: str, file: UploadFile):
    ext = Path(file.filename).suffix.lower()

    s3.put_object(
        Body=file.file,
        Bucket=bucket_name,
        Key=f"videos/{video_id}/main{ext}"
    )

########## Get Video - Signed ##########
async def get_presigned_url(video_id: str, file_name: str):
    key = f"videos/{video_id}/{file_name}"

    url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {
            "Bucket": bucket_name,
            "Key": key
        },
        ExpiresIn = settings.STREAM_EXPIRE_MINUTES * 60
    )

    return url
