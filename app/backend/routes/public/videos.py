########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Video, Video_Status, User_Channel, User_Follow

from core.config import settings

from core.utils.http_requests import post_data
from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.generator import get_uuid, get_short_id
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, read_params, validate_required_fields, validate_user

########## Variables ##########
router = APIRouter()

########## Get Video ##########
@router.get("/watch/{id}")
async def watch_video(request: Request, id: str, db: Session = Depends(get_db)):
    ### Validations ###
    video = db.query(Video).filter(Video.short_id == id).first()

    if not video:
        return custom_response(status_code=400, message="The video does not exist")

    res = await post_data("/videos/get-video", {
        "video_id": video.id,
        "video_status": video.status,
    })

    url = res["data"]["video_url"]

    channel = db.query(User_Channel).filter(User_Channel.id == video.channel_id).first()
    followers = db.query(User_Follow).filter(User_Follow.channel_id == channel.id).count()

    return custom_response(status_code=200, message="IDK", data={
        "video_source": url,
        "video": {
            "short_id": video.short_id,
            "title": video.title,
            "status": video.status,
            "description": video.description,

            "views": video.views,
            "likes": video.likes,
            "dislikes": video.dislikes,
            
            "date": video.date
        },
        "channel": {
            "tag": channel.tag,
            "name": channel.name,
            "followers": followers,
            "avatar": channel.avatar_url,
        }
    })

########## Newest Videos ##########
@router.get("/newest")
async def home(request: Request, db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.status == Video_Status.ready).order_by(desc(Video.date)).limit(10).all()

    videos_data = []

    for video in videos:
        channel = db.query(User_Channel).filter(User_Channel.id == video.channel_id).first()
        videos_data.append({
            "short_id": video.short_id,
            "title": video.title,
            "views": video.views,

            "channel_tag": channel.tag,
            "channel_name": channel.name,
            "channel_avatar": channel.avatar_url,
        })

    return custom_response(status_code=200, message="Newest Videos", data={
        "videos": videos_data
    })