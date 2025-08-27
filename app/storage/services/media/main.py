########## Modules ##########
import os

from pathlib import Path

from core.config import settings
from core.utils.http_requests import post_download_file, post_data_api, post_data, post_signed_url

########## Download Video ##########
async def download_file(video_id: str, file_path: str):
    try:        
        await post_download_file("/download", { "location": file_path })
    except Exception as e:
        print(e)

########## Delete Video ##########
async def delete_file(video_id: str):
    try:
        print("deleting")
            # await s3.delete_object(Bucket=bucket_name, Key=f"videos/{video_id}/main.mp4")
    except Exception as e:
        print(e)

########## Upload files ##########
async def upload_files(video_id: str, file_path: str):
    try:
        print(file_path)
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.endswith(".mp4"):
                    continue
                
                file_paths = os.path.join(root, file)
                location = f"videos/{video_id}"
                filename = os.path.basename(file_paths)

                with open(file_paths, "rb") as f:
                    file_bytes = f.read()

                await post_data("/upload", file_bytes, { "location": location, "filename": filename })
                    
    except Exception as e:
        print(e)

########## Get Video - Signed ##########
# async def get_presigned_url(video_id: str, file_name: str):
#     location = f"videos/{video_id}/{file_name}"

#     try:
#         res = await post_signed_url("/get-file-url", { "location": location })

    
#     except Exception as e:
#         print(e)
