########## Modules ##########
import shutil

from pathlib import Path

from fastapi import APIRouter, Depends, Request, UploadFile, File

from core.config import settings

from core.utils.converter import queue
from core.utils.responses import custom_response
from core.utils.http_requests import post_data_api
from core.utils.validators import read_json_body, validate_required_fields

from services.media.main import download_file

########## Variables ##########
router = APIRouter()
allowed_exts = [".mp4"]

########## Upload video ##########
@router.post("/upload")
async def upload_video(request: Request):
    ### Get Body ###
    video, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)
    
    ### Validations ###
    required_fields, error = validate_required_fields(video, ["video_id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    video_id = video.video_id

    ### Save File ###
    SAVE_DIR = request.app.state.SAVE_DIR
    temp_dir = SAVE_DIR / video_id
    temp_dir.mkdir(parents=True, exist_ok=True)
    local_path = temp_dir / "main.mp4"

    await download_file(video_id, f"videos/{video_id}/main.mp4")

    await queue.put({
        "video_id": video_id,
        "dir": temp_dir,
        "video_dir": local_path
    })

    return custom_response(status_code=200, message="Video uploaded!")
