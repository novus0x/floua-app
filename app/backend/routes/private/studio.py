########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Channel, User_Follow, Video, Video_Source_type, Video_Visibility, Video_Status

from core.config import settings

from core.utils.http_requests import post_data
from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.generator import get_uuid, get_short_id
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, read_params, validate_required_fields, validate_user

########## Variables ##########
router = APIRouter()

########## Manage Channels ##########
@router.get("/manage/channels")
async def manage_channels(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Variables ###
    channels = []

    channels_data = db.query(User_Channel).filter(User_Channel.user_id == user["id"]).order_by(desc(User_Channel.date)).all()

    for channel in channels_data:
        followers = db.query(User_Follow).filter(User_Follow.channel_id == channel.id).count()

        channels.append({
            "id": channel.id,

            "name": channel.name,
            "tag": channel.tag,
            "followers": followers,

            "date": channel.date
        })


    return custom_response(status_code=200, message="Manage Channels", data={
        "channels": channels
    })

########## Get Channel ##########
@router.get("/manage/channels/{tag}")
async def manage_channels(request: Request, tag: str, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    channel = db.query(User_Channel).filter(User_Channel.tag == tag).first()

    if not channel:
        return custom_response(status_code=400, message="The channel doesn't exist")

    if user["id"] != channel.user_id:
        return custom_response(status_code=400, message="You don't have access to this channel")

    followers = db.query(User_Follow).filter(User_Follow.channel_id == channel.id).count()
    views = 0
    points = 0
    videos = db.query(Video).filter(Video.channel_id == channel.id).count()
    latest_videos = []

    latest_videos_data = db.query(Video).filter(Video.user_id == user["id"]).order_by(desc(Video.date)).limit(10).all()

    for video in latest_videos_data:
        latest_videos.append({
            "short_id": video.short_id,
            "title": video.title,
            "status": video.status,
            "visibility": video.visibility,
            "views": video.views,
            "popularity": "N/A",
            "comments": video.comments_count
        })    

    data = {
        "views": views,
        "followers": followers,
        "points": points,
        "videos": videos,
        "latest_videos": latest_videos,
    }

    return custom_response(status_code=200, message="Manage Channels", data={
        "channel": data,
    })

########## Upload Video ##########
@router.post("/channel/{tag}/upload")
async def upload_video_info(request: Request, tag: str, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    channel = db.query(User_Channel).filter(User_Channel.tag == tag).first()

    if not channel:
        return custom_response(status_code=400, message="The channel doesn't exist")

    if user["id"] != channel.user_id:
        return custom_response(status_code=400, message="You don't have access to this channel")

    ### Get Body ###
    video_info, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(video_info, ["title", "description", "visibility", "contract", "source"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    new_video = Video(
        id = await get_uuid(Video, db),
        short_id = await get_short_id(Video, db),
        title = video_info.title,
        description = video_info.description,
        visibility = video_info.visibility,

        user_id = user["id"],
        channel_id = channel.id,
    )

    if video_info.source == "cdn": new_video.source_type = Video_Source_type.cdn
    elif video_info.source == "youtube": new_video.source_type = Video_Source_type.youtube
    elif video_info.source == "external": new_video.source_type = Video_Source_type.external

    if video_info.visibility == "public": new_video.visibility = Video_Visibility.public
    elif video_info.visibility == "private": new_video.visibility = Video_Visibility.private
    elif video_info.visibility == "unlisted": new_video.visibility = Video_Visibility.unlisted

    res = await post_data("/videos/generate_upload_token", {"video_id": new_video.id})

    if not res.get("data", {}).get("upload_token"): 
        return custom_response(status_code=400, message="Something went wrong, please try again later!")

    token = res.get("data", {}).get("upload_token")

    add_db(db, new_video)

    return custom_response(status_code=200, message="Perfect", data={
        "destination": settings.CDN_ORIGIN + "/videos/upload",
        "upload_token": token,
        "short_id": new_video.short_id,
    })

########## Update Video Upload Status ##########
@router.post("/video-upload-status")
async def upload_video_info(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    video_info, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(video_info, ["video_id", "video_status"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    video = db.query(Video).filter(Video.id == video_info.video_id).first()

    if not video:
        return custom_response(status_code=400, message="Something went wrong")

    video.status = Video_Status.error

    if video_info.video_status == "uploaded": video.status = Video_Status.uploaded
    elif video_info.video_status == "processing": video.status = Video_Status.processing
    elif video_info.video_status == "ready": video.status = Video_Status.ready

    update_db(db)

    return custom_response(status_code=200, message="Updated!")