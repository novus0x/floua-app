########## Modules ##########
import os, aioboto3

from pathlib import Path

from core.config import settings

########## Variables ##########
session  = aioboto3.Session()
bucket_name = settings.WASABI_BUCKET_NAME

########## WASABI ##########
async def get_s3():
    return session.client('s3',
    endpoint_url="https://s3.us-central-1.wasabisys.com",
    region_name="us-central-1",
    aws_access_key_id=settings.WASABI_ACCESS_KEY,
    aws_secret_access_key=settings.WASABI_SECRET_KEY,
)

########## Download Video ##########
async def download_file(video_id: str, file_path: str):
    try:
        async with await get_s3() as s3:
            await s3.download_file(bucket_name, f"videos/{video_id}/main.mp4", file_path)
    except Exception as e:
        print(e)

########## Delete Video ##########
async def delete_file(video_id: str):
    try:
        print("deleting")
        async with await get_s3() as s3:
            await s3.delete_object(Bucket=bucket_name, Key=f"videos/{video_id}/main.mp4")
    except Exception as e:
        print(e)

########## Upload files ##########
async def upload_files(video_id: str, file_path: str):
    try:
        async with await get_s3() as s3:
            for root, _, files in os.walk(file_path):
                for file in files:
                    if file.endswith(".mp4"):
                        continue
                    
                    file_paths = os.path.join(root, file)
                    relative_path = os.path.relpath(file_paths, file_path)
                    s3_key = f"videos/{video_id}/{relative_path}".replace("\\", "/")

                    with open(file_paths, "rb") as f:
                        await s3.put_object(Bucket=bucket_name, Key=s3_key, Body=f)
    except Exception as e:
        print(e)

########## Get Video - Signed ##########
async def get_presigned_url(video_id: str, file_name: str):
    key = f"videos/{video_id}/{file_name}"

    try:
        async with await get_s3() as s3:
            url = await s3.generate_presigned_url(
                ClientMethod = 'get_object',
                Params = {
                    "Bucket": bucket_name,
                    "Key": key
                },
                ExpiresIn = settings.STREAM_EXPIRE_MINUTES * 60
            )

            return url
    
    except Exception as e:
        print(e)
