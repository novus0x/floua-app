########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Video, Video_Status, Video_Visibility, User_Channel, User_Follow, User, Comment

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

########## Create Comment ##########
@router.post("/comments/{id}")
async def get_channel(request: Request, id: str, db: Session = Depends(get_db)):
    ### Validations ###
    video = db.query(Video).filter(Video.short_id == id).first()

    if not video:
        return custom_response(status_code=400, message="The video does not exist")
    
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message="You need to signin to add a comment")
    
    ### Get Body ###
    comment, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(comment, ["content", "parent_id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    parent_id_value = None
    print(comment.content)

    if comment.parent_id != "none":
        print("Do something!")

    new_comment = Comment(
        id = get_uuid(Comment, db),
        content = comment.content,

        video_id = video.id,
        user_id = user["id"],
        parent_id = parent_id_value
    )

    add_db(db, new_comment)
    
    return custom_response(status_code=200, message="Comment added!")

########## Get Comments ##########
@router.get("/comments/{id}")
async def get_channel(request: Request, id: str, db: Session = Depends(get_db)):
    ### Validations ###
    video = db.query(Video).filter(Video.short_id == id).first()

    if not video:
        return custom_response(status_code=400, message="The video does not exist")
    
    ### Get params ###
    query = await read_params(request)

    # if not query["tag"]:
    #     return custom_response(status_code=400, message="The channel does not exist")

    comments = db.query(Comment).filter(Comment.video_id == video.id).order_by(desc(Comment.date)).all()

    comments_data = []

    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()

        if user:
            comments_data.append({
                "id": comment.id,
                "content": comment.content,
                "parent_id": comment.parent_id,
                "date": comment.date,

                "user": {
                    "id": user.id,
                    "username": user.username,
                    "avatar_url": user.avatar_url
                }
            })
    
    return custom_response(status_code=200, message="Comments", data={
        "comments": comments_data
    })

########## Newest Videos ##########
@router.get("/newest")
async def newest_videos(request: Request, db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.status == Video_Status.ready).order_by(desc(Video.date)).limit(10).all()

    videos_data = []

    for video in videos:
        channel = db.query(User_Channel).filter(User_Channel.id == video.channel_id).first()
        videos_data.append({
            "short_id": video.short_id,
            "title": video.title,
            "views": video.views,
            "thumbnail_url": video.thumbnail_url,

            "channel_tag": channel.tag,
            "channel_name": channel.name,
            "channel_avatar": channel.avatar_url,
        })

    return custom_response(status_code=200, message="Newest Videos", data={
        "videos": videos_data
    })

########## Newest Videos From Channel ##########
@router.get("/newest/{tag}")
async def newest_videos_channel(request: Request, tag: str, db: Session = Depends(get_db)):
    ### Validate Channel ###
    channel = db.query(User_Channel).filter(User_Channel.tag == tag).first()

    if not channel:
        return custom_response(status_code=400, message="The channel does not exist")

    ### Get Videos ###
    videos = db.query(Video).filter(
        Video.status == Video_Status.ready,
        # Video.visibility == Video_Visibility.public,
        Video.channel_id == channel.id,
    ).order_by(desc(Video.date)).limit(10).all()

    videos_data = []

    for video in videos:
        channel = db.query(User_Channel).filter(User_Channel.id == video.channel_id).first()
        videos_data.append({
            "short_id": video.short_id,
            "title": video.title,
            "views": video.views,
            "thumbnail_url": video.thumbnail_url,

            "channel_tag": channel.tag,
            "channel_name": channel.name,
            "channel_avatar": channel.avatar_url,
        })

    return custom_response(status_code=200, message="Newest Videos", data={
        "videos": videos_data
    })

########## Popular Videos From Channel ##########
@router.get("/popular/{tag}")
async def popular_videos_channel(request: Request, tag: str, db: Session = Depends(get_db)):
    ### Validate Channel ###
    channel = db.query(User_Channel).filter(User_Channel.tag == tag).first()

    if not channel:
        return custom_response(status_code=400, message="The channel does not exist")

    ### Get Videos ###
    videos = db.query(Video).filter(
        Video.status == Video_Status.ready,
        # Video.visibility == Video_Visibility.public,
        Video.channel_id == channel.id,
    ).order_by(desc(Video.likes - Video.dislikes)).limit(10).all()

    videos_data = []

    for video in videos:
        channel = db.query(User_Channel).filter(User_Channel.id == video.channel_id).first()
        videos_data.append({
            "short_id": video.short_id,
            "title": video.title,
            "views": video.views,
            "thumbnail_url": video.thumbnail_url,

            "channel_tag": channel.tag,
            "channel_name": channel.name,
            "channel_avatar": channel.avatar_url,
        })

    return custom_response(status_code=200, message="Popular Videos", data={
        "videos": videos_data
    })
