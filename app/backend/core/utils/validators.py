########## Modules ##########
import json, uuid, random, string, datetime

from types import SimpleNamespace

from fastapi import Request
from sqlalchemy.orm import Session

from db.model import Allowed_Email_Domain, User_Session, User

from core.config import settings
from core.utils.encrypt import check_jwt
from core.utils.db_management import add_db, update_db

########## Read Json body ##########
async def read_json_body(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        obj = SimpleNamespace(**data)
        return obj, None
    except json.JSONDecodeError:
        return None, "Invalid Json"

########## Validate required fields  ##########
def validate_required_fields(data: dict, fields: list):
    required_fields = []

    for field in fields:
        clean_name = [field.replace("_", " ")]
        if not hasattr(data, field):
            required_fields.append({"field": field, "message": str(clean_name[0].capitalize()) + " is required"})
        else:
            value = getattr(data, field)
            if not isinstance(value, str) or value.strip() == "":
                required_fields.append({"field": field, "message": str(clean_name[0].capitalize()) + " is required"})
    
    if len(required_fields) > 0:
        return required_fields, True

    return None, False

########## Check email domain ##########
async def validate_email_domain(email: str, db: Session):
    email_domain = email.split("@")

    if len(email_domain) > 2:
        return False

    if db.query(Allowed_Email_Domain).filter(Allowed_Email_Domain.domain == email_domain[1]).first():
        return True

    return False

########## Get token ##########
async def get_token(request, db: Session, required = False):
    token = request.cookies.get(settings.TOKEN_NAME)
    if not token:
        return None, True

    if required == False:
        return {}, None

    token_data, error = check_jwt(token)

    if error:
        return None, "Invalid token"

    user_session = db.query(User_Session).filter(User_Session.id == token_data["session_id"]).first()
    
    if not user_session:
        return None, "Invalid token"

    return token_data["session_id"], False

########## Get user ##########
async def validate_user(request, db: Session, required = False):
    token = request.cookies.get(settings.TOKEN_NAME)
    if not token:
        return None, True

    if required == False:
        return {}, None

    token_data, error = check_jwt(token)

    if error:
        return None, "Invalid token"

    user_session = db.query(User_Session).filter(User_Session.id == token_data["session_id"]).first()
    
    if not user_session:
        return None, "Invalid token"

    if not user_session.is_active:
        return None, "The session has expired"
    
    current_date = datetime.datetime.utcnow()

    if user_session.expires_at != None:
        expiration_date = user_session.expires_at 
        
        if expiration_date <= current_date:
            user_session.is_active = False
            update_db(db)
            return None, "The session has expired"
    
    user_session.last_used_at = current_date
    update_db(db)

    user_data = db.query(User).filter(User.id == user_session.user_id).first()
    
    user = {
        "id": user_data.id,
        "username": user_data.username,
        "email": user_data.email,
        "points" : user_data.points,

        "avatar_url" : user_data.avatar_url,
        "bio": user_data.bio,

        "email_verified" : user_data.email_verified,
        "has_channel": user_data.has_channel,
        "user_session_extra" : user_data.user_session_extra,

        "date" : user_data.date,
    }

    return user, False
