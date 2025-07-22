########## Modules ##########
import json, uuid, random, string, datetime
from types import SimpleNamespace

from fastapi import Request
from sqlalchemy.orm import Session

from db.model import Allowed_Email_Domain, User_Session, User

from core.utils.encrypt import check_jwt

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
        if not hasattr(data, field):
            required_fields.append({"field": field, "message": field + " is required"})
        else:
            value = getattr(data, field)
            if not isinstance(value, str) or value.strip() == "":
                required_fields.append({"field": field, "message": field + " is required"})
    
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

########## Get user ##########
async def get_user(headers, db: Session, required = False):
    if "Authorization" not in headers:
        return None, True

    token = headers["Authorization"]

    if required == False:
        return {}, None

    token_data, error = check_jwt(token)

    if error:
        return None, "Invalid token"

    user_session = db.query(User_Session).filter(User_Session.id == token_data["session_id"]).first()

    if not user_session.is_active:
        return None, "The session has expired"
    
    current_date = datetime.datetime.utcnow()

    if user_session.expires_at != None:
        expiration_date = user_session.expires_at 
        
        if expiration_date <= current_date:
            user_session.is_active = False
            db.commit()
            return None, "The session has expired"
    
    user_session.last_used_at = current_date
    db.commit()

    user_data = db.query(User).filter(User.id == user_session.user_id).first()
    
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "bio": user_data.bio,
        "points" : user_data.points,

        "display_name" : user_data.display_name,
        "avatar_url" : user_data.avatar_url,

        "email_verified" : user_data.email_verified,
        "user_session_extra" : user_data.user_session_extra,

        "date" : user_data.date,
    }

    return user, False
