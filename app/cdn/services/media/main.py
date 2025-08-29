########## Modules ##########
from pathlib import Path

from fastapi import UploadFile

from core.config import settings
from core.utils.http_requests import post_data_media, post_signed_url

########## Download Video ##########
async def download_file(video_id: str, file_path: str):
    try:        
        await download_file("/download", { "location": file_path })
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
async def upload_original_video(video_id: str, file: UploadFile):
    try:
        ext = Path(file.filename).suffix.lower()

        location = f"videos/{video_id}"

        await post_data_media("/upload", file, { "location": location, "filename": "main.mp4" })
                    
    except Exception as e:
        print(e)

########## Upload Thumbnail ##########
async def upload_thumbnail(video_id: str, file: UploadFile, ext: str):
    print("uploading thumbnail")
    try:
        ext = Path(file.filename).suffix.lower()

        location = f"videos/{video_id}"

        await post_data_media("/upload", file, { "location": location, "filename": f"thumbnail{ext}" })
        return location + f"/thumbnail{ext}"

    except Exception as e:
        print(e)

########## Media Service - Signed url ##########
async def get_presigned_url(endpoint: str, data: dict):
    try:
        url = await post_signed_url(endpoint, data)
        return url

    except Exception as e:
        print(e)