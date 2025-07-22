########## Modules ##########
import datetime

from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Session

from core.utils.generator import get_uuid
from core.utils.responses import custom_response
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, validate_required_fields, validate_email_domain

########## Variables ##########
router = APIRouter()

########## Signup ##########
@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    user, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(user, ["username", "email", "password", "confirm_password", "birth"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)
        
    email_check = await validate_email_domain(user.email, db)
    if not email_check: 
        return custom_response(status_code=400, message="Invalid email domain")

    if db.query(User).filter(User.email == user.email).first():
        return custom_response(status_code=400, message="Email already registered")

    if db.query(User).filter(User.username == user.username).first():
        return custom_response(status_code=400, message="Username already in use")

    if user.password != user.confirm_password:
        return custom_response(status_code=400, message="Passwords don't match")

    ### Save to DB ###
    new_user = User(
        id = await get_uuid(User, db),
        username = user.username.lower(),
        email = user.email,
        password = hash_password(user.password),
        birth = user.birth
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return custom_response(status_code=201, message="User created")

########## Signin ##########
@router.post("/signin")
async def signup(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    user, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(user, ["email", "password", "expires", "ip_addr", "user_agent", "location", "device_name"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    user_data = db.query(User).filter(User.email == user.email).first()

    if not user_data:
        return custom_response(status_code=401, message="Invalid credentials")

    if not check_password(user_data.password, user.password):
        return custom_response(status_code=401, message="Invalid credentials")
    
    ### Save to DB ###
    new_session = User_Session(
        id = await get_uuid(User_Session, db),
        user_id = user_data.id,
        expires_at = None,
    )

    if user.expires == "1": 
        new_session.expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)

    if user_data.user_session_extra:
        new_session.ip_addr = user.ip_addr
        new_session.user_agent = user.user_agent
        new_session.location = user.location
        new_session.device_name = user.device_name

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    token = generate_jwt(session_id=new_session.id, expires=user.expires)

    return custom_response(status_code=200, message="Login successful", data={"token": token})
