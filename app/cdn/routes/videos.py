########## Modules ##########
import json, websockets, datetime

from pathlib import Path

from fastapi import APIRouter, Depends, Request, WebSocket, UploadFile, File

from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Video

from core.utils.responses import custom_response
from core.utils.generator import get_uuid, build_signed_url
from core.utils.validators import read_json_body, validate_required_fields
from core.utils.ws import broadcast_all_nodes

from routes.nodes import connected_nodes

########## Variables ##########
router = APIRouter()
WS_URL = "ws://192.168.1.36:3003"
allowed_exts = [".mp4", ".mov", ".mkv"]

########## Generate upload token ##########
@router.post("/generate_upload_token")
async def generate_upload_token(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    user, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(user, ["video_id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    await broadcast_all_nodes("Hola desde generating", connected_nodes)

    print(connected_nodes)

    ### Send data ###
    return "ok"

########## Upload video ##########
@router.post("/upload")
async def upload_video(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ### Get data ###
    form = await request.form()

    video_id = form.get("video_id")
    upload_token = form.get("upload_token")
    ext = Path(file.filename).suffix.lower()

    ### Validations ###
    if db.query(Video).filter(Video.id == video_id).first():
        return custom_response(status_code=400, message="video_id already in use")

    if not video_id or not upload_token:
        return custom_response(status_code=400, message="video_id and upload_token are required")

    if ext not in allowed_exts:
        return custom_response(status_code=400, message="Invalid extention")

    ### Upload video ###
    try:
        async with websockets.connect(WS_URL) as ws:
            video_information = {
                "type": "upload_init",
                "video_info": {
                    "video_id": video_id,
                    "filename": file.filename,
                    "content_type": file.content_type or "video/mp4"
                }
            }

            try:
                json_msg = json.dumps(video_information)

                await ws.send(json_msg)

                while True:
                    chunk = await file.read(1024 * 1024)

                    if not chunk:
                        break

                    await ws.send(chunk)
                
                json_msg = json.dumps({
                    "type": "upload_end"
                })
                await ws.send(json_msg)

                new_video = Video(id = video_id)
                db.add(new_video)
                db.commit()
                db.flush(new_video)
                return custom_response(message="Upload end", status_code=201)

            except Exception as e:
                return custom_response(status_code=400, message="Error while uploading file")

    except Exception as e: ### Error - Node not available
        return custom_response(status_code=400, message="Node not available")