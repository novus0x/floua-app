########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Session, User_Session

from core.utils.generator import get_uuid
from core.utils.db_management import update_db
from core.utils.responses import custom_response
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, validate_required_fields, validate_email_domain, validate_user, get_token

########## Variables ##########
router = APIRouter()

########## Validate ##########
@router.get("/validate")
async def validate(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    return custom_response(status_code=200, message="Account information", data={
        "user": user
    })

########## Login Tracking ##########
@router.get("/login-tracking")
async def login_tracking_get(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    login_tracking_sessions = db.query(User_Session).filter(User_Session.user_id == user["id"]).order_by(desc(User_Session.date)).limit(10).all()

    sessions = []

    for session in login_tracking_sessions:
        parser = None
        
        if session.user_agent:
            parser = parse(session.user_agent)

        sessions.append({
            "id": session.id,

            "is_active": session.is_active,
            "expires_at": session.expires_at,

            "ip_addr": session.ip_addr,
            "user_agent": session.user_agent,
            "location": session.location if session.location else "Unknown",

            "last_used_at": session.last_used_at,
            "date": session.date,

            "os_name": parser.os.family if parser else "Unknown",
            "os_version": parser.os.version_string if parser else "Unknown",
            "device_name": parser.device.family if parser else "Unknown",
            "device_vendor": parser.device.brand if parser else "Unknown",
            "device_model": parser.device.model if parser else "Unknown",
            "device_mobile": parser.is_mobile if parser else "Unknown",
            "device_tablet": parser.is_tablet if parser else "Unknown",
            "device_pc": parser.is_pc if parser else "Unknown",
            "browser_name": parser.browser.family if parser else "Unknown",
            "browser_version": parser.browser.version_string if parser else "Unknown",
        })

    return custom_response(status_code=200, message="Login tracking information", data={
        "sessions": sessions
    })

########## Activate or Deactivate Loggin Tracking ##########
@router.post("/login-tracking")
async def login_tracking_post(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    session, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(session, ["login_tracking_option"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)
    
    session_data = db.query(User).filter(User.id == user["id"]).first()

    if not session_data:
        return custom_response(status_code=400, message="Invalid session")

    session_data.user_session_extra = True if session.login_tracking_option == "1" else False
    update_db(db)

    return custom_response(status_code=200, message="Login Tracking option updated")

########## Deactivate session ##########
@router.post("/deactivate-session")
async def validate(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    session, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(session, ["session_id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)
    
    session_data = db.query(User_Session).filter(User_Session.id == session.session_id).first()

    if not session_data:
        return custom_response(status_code=400, message="Invalid session")

    session_data.is_active = False
    update_db(db)

    token, error = await get_token(request, db, True)
    
    current_session = False
    if token == session.session_id:
        current_session = True

    return custom_response(status_code=200, message="Session deactivated successfully", data={
        "current_session": current_session,
    })