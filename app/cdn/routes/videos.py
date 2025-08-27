########## Modules ##########
import datetime

from pathlib import Path

from fastapi import APIRouter, Depends, Request, UploadFile, File

from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Video, Upload_Token

from core.config import settings

from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.encrypt import hash_token, check_token
from core.utils.generator import get_uuid, build_signed_url
from core.utils.http_requests import post_data, post_data_api
from core.utils.validators import read_json_body, validate_required_fields

from services.media.main import upload_original_video, get_presigned_url

########## Variables ##########
router = APIRouter()
WS_URL = "ws://192.168.1.80:3003"
allowed_exts = [".mp4"] # , ".mov", ".mkv"

########## Generate Signed Video URL ##########
@router.post("/get-video")
async def get_video(request: Request):
    ### Get Body ###
    video, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(video, ["video_id", "video_status"])

    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    file_name = "main.mp4"

    if video.video_status == "ready": 
        file_name = "master.m3u8"
    
    location = f"videos/{video.video_id}/{file_name}"
    
    url = await get_presigned_url("/get-file-url", { "location": location })

    return custom_response(status_code=200, message="Signed Video URL", data={
        "video_url": url,
    })


########## Generate upload token ##########
@router.post("/generate_upload_token")
async def generate_upload_token(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    video, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(video, ["video_id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    if db.query(Video).filter(Video.id == video.video_id).first():
        return custom_response(status_code=400, message="The video is already in DB")

    upload_token_id = await get_uuid(Upload_Token, db)
    hashed_token = hash_token(str(upload_token_id))

    new_upload_token = Upload_Token(
        id = upload_token_id,
        video_id = video.video_id,
        token = hashed_token,
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.UPLOAD_EXPIRE_MINUTES),
    )
    add_db(db, new_upload_token)

    ### Send data ###
    return custom_response(status_code=200, message="Upload token generated", data={
        "upload_token": new_upload_token.token
    })

########## Upload video ##########
@router.post("/upload")
async def upload_video(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ### Get data ###
    form = await request.form()

    # video_id = form.get("video_id")
    upload_token = form.get("upload_token")
    ext = Path(file.filename).suffix.lower()

    ### Validations ###
    if not upload_token:
        return custom_response(status_code=400, message="video_id and upload_token are required")

    upload_token_data = db.query(Upload_Token).filter(Upload_Token.token == upload_token).first()
    if not upload_token_data:
        return custom_response(status_code=400, message="Invalid upload_token")
    
    video_id = upload_token_data.video_id

    if db.query(Video).filter(Video.id == video_id).first():
        return custom_response(status_code=400, message="video_id already in use")

    if upload_token_data.used == True:
        return custom_response(status_code=400, message="Token already used")

    current_date = datetime.datetime.utcnow()
    expiration_date = upload_token_data.expires_at 

    if upload_token_data.expired == True:
        return custom_response(status_code=400, message="The session has already expired")
        
    elif expiration_date <= current_date:
        upload_token_data.expired = True
        db.commit()
        return custom_response(status_code=400, message="The session has already expired")

    if ext not in allowed_exts:
        return custom_response(status_code=400, message="Invalid extention")

    ### Upload video ###
    upload_token_data.used = True ### Token used
    update_db(db)

    await upload_original_video(video_id, file)
    await post_data("/videos/upload", {
        "video_id": video_id,
    })
    await post_data_api("/api/studio/video-upload-status", {
        "video_id": video_id,
        "video_status": "uploaded"
    })
    
    return custom_response(status_code=200, message="Video uploaded!")
