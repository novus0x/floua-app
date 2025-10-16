########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Channel, User_Follow, User_Role, Video

from core.utils.generator import get_uuid
from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, read_params, validate_required_fields, validate_user

########## Variables ##########
router = APIRouter()

########## Get channel ##########
@router.get("/get")
async def get_channel(request: Request, db: Session = Depends(get_db)):
    ### Get params ###
    query = await read_params(request)
    
    if not query["tag"]:
        return custom_response(status_code=400, message="The channel does not exist")

    ### Get Session ###
    user, error = await validate_user(request, db, True)

    ### Get Channel ###
    channel = db.query(User_Channel).filter(User_Channel.tag == query["tag"]).first()

    if not channel:
        return custom_response(status_code=400, message="The channel does not exist")

    creator_id = ""

    if not error:
        if channel.user_id == user["id"]:
            creator_id = user["id"]

    followers = db.query(User_Follow).filter(User_Follow.channel_id == channel.id).count()
    videos = db.query(Video).filter(Video.channel_id == channel.id).count()

    channel = {
        "name": channel.name,
        "description": channel.description,
        "tag": channel.tag,
        "avatar_url": channel.avatar_url,
        "user_id": channel.user_id,
        "date": channel.date,
    }

    return custom_response(status_code=200, message="Channel info", data={
        "channel": channel,
        "followers": followers,
        "videos": videos,
    })

########## Create channel ##########
@router.post("/create")
async def create_channel(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    channel, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(channel, ["name", "tag", "description"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    user_channels_q = db.query(User_Channel).filter(User_Channel.user_id == user["id"]).count()

    if user_channels_q >= 2:
        return custom_response(status_code=400, message="You have the maximum number of channels allowed")

    channel_exists = db.query(User_Channel).filter(User_Channel.tag == channel.tag).first()

    if channel_exists:
        return custom_response(status_code=400, message="The channel name is already in use")

    if not user["has_channel"]:
        update_user = db.query(User).filter(User.id == user["id"]).first()
        update_user.has_channel = True
        update_user.role = User_Role.creator
        update_db(db)

    new_channel = User_Channel(
        id = get_uuid(User_Channel, db),
        user_id = user["id"],

        tag = channel.tag,
        name = channel.name,
        description = channel.description,
    )

    add_db(db, new_channel)

    return custom_response(status_code=200, message="Channel created")
