########## Modules ##########
from datetime import timezone, datetime, timedelta

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Session, User_Verification

from core.config import settings

from core.utils.geoip import lookup_ip
from core.utils.generator import get_uuid
from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.encrypt import hash_password, check_password, generate_jwt, check_jwt
from core.utils.validators import read_json_body, validate_required_fields, validate_email_domain, validate_user

from services.smtp.main import template_routes, get_html, send_mail

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
    required_fields, error = validate_required_fields(user, ["username", "email", "password", "confirm_password", "date_of_birth"])
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

    ### Improve Password ###
    if len(user.password) < 12:
        return custom_response(status_code=400, message="The password must be at least 12 characters long for security reasons")

    ### Validate Age ###
    birth_year = datetime.fromisoformat(user.date_of_birth).date()
    today = datetime.utcnow().date()

    try:
        max_date = today.replace(year=today.year - 124) - timedelta(days=164)
    except ValueError:
        max_date = today.replace(month=2, day=28, year=today.year - 124) - timedelta(days=164)

    if birth_year < max_date:
        return custom_response(status_code=400, message="It is impossible to live that long, are you sure that you still alive? :|")

    ### Save to DB ###
    new_user = User(
        id = get_uuid(User, db),
        username = user.username.lower(),
        email = user.email,
        password = hash_password(user.password),
        birth = user.date_of_birth
    )
    add_db(db, new_user)

    html_body = await get_html(template_routes.auth.welcome, {
        "username": new_user.username,
        "role": "Viewer"
    })

    # await send_mail("noreply", "Registration on Floua - Dev", new_user.email, html_body)

    return custom_response(status_code=201, message="User created")

########## Signin ##########
@router.post("/signin")
async def signup(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    user, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(user, ["email", "password", "expires"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    user_data = db.query(User).filter(User.email == user.email).first()

    if not user_data:
        return custom_response(status_code=400, message="Invalid credentials")

    if not check_password(user_data.password, user.password):
        return custom_response(status_code=400, message="Invalid credentials")
    
    ### Save to DB ###
    new_session = User_Session(
        id = get_uuid(User_Session, db),
        user_id = user_data.id,
        expires_at = None,
    )

    if user.expires == "0": 
        new_session.expires_at = datetime.now(timezone.utc) + timedelta(days=15)

    ### Geo IP ###
    if user_data.user_session_extra:
        forwarded = request.headers.get("x-formwarded-for")
        ip_addr = forwarded.split(",")[0].strip() if forwarded else request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        ip_info = lookup_ip(ip_addr)

        new_session.ip_addr = ip_addr
        new_session.user_agent = user_agent
        new_session.location = str(ip_info)

    add_db(db, new_session)

    token = generate_jwt(session_id=new_session.id, expires=user.expires)

    response = custom_response(status_code=200, message="Login successful")
    response.set_cookie(
        key = settings.TOKEN_NAME,
        value = token,
        httponly = True,
        secure = False, # Prod --> True
        max_age = new_session.expires_at,
    )
    return response

########## Logout ##########
@router.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(settings.TOKEN_NAME)
    token_data, error = check_jwt(token)

    if token_data:
        user_session = db.query(User_Session).filter(User_Session.id == token_data["session_id"]).first()

        if user_session:
            user_session.is_active = False
            update_db(db)

    response = custom_response(status_code=200, message="Logout successful")
    response.delete_cookie(key=settings.TOKEN_NAME)
    return response

########## Verify Account - GET ##########
@router.get("/verify")
async def validate(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    verifications = db.query(User_Verification).filter(User_Verification.user_id == user["id"]).order_by(desc(User_Verification.date)).all()

    if len(verifications) > 0:
        for verification in verifications:
            current_date = datetime.now(timezone.utc)
            verification_date = verification.date

            time_aprx = current_date - verification_date
            minutes = abs(time_aprx.total_seconds()) / 60

            if minutes < 2:
                return custom_response(status_code=400, message="Try again later. Hint: 2 minutes after your last try")

    new_verification = User_Verification(
        id = get_uuid(User_Verification, db),
        user_id = user["id"],
    )

    new_verification.expires_at = datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
    add_db(db, new_verification)

    html_body = await get_html(template_routes.auth.verify, {
        "verification_route": settings.FRONTEND_ORIGIN + "/auth/verify/" +  new_verification.id
    })

    await send_mail("noreply", "Account Verification - Dev", user["email"], html_body)

    return custom_response(status_code=200, message="Verifiction link sent, check your email")

########## Verify Account - POST ##########
@router.post("/verify")
async def validate(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    verify, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(verify, ["id"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)
    
    verification = db.query(User_Verification).filter(User_Verification.id == verify.id).first()

    if not verification:
        return custom_response(status_code=400, message="Invalid link")

    if verification.used:
        return custom_response(status_code=400, message="Invalid link")
    
    current_date = datetime.now(timezone.utc)
    expiration_date = verification.expires_at
        
    if expiration_date <= current_date:
        verification.used = True
        update_db(db)
        return custom_response(status_code=400, message="Invalid link")

    user = db.query(User).filter(User.id == verification.user_id).first()

    if not user:
        return custom_response(status_code=400, message="Invalid link")

    user.email_verified = True
    verification.used = True
    update_db(db)

    return custom_response(status_code=200, message="Account verified", data={})
