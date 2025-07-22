########## Modules ##########
from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, User_Session

from core.utils.generator import get_uuid
from core.utils.responses import custom_response
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, validate_required_fields, validate_email_domain, get_user

########## Variables ##########
router = APIRouter()

########## My Account ##########
@router.get("/me")
async def me(request: Request, db: Session = Depends(get_db)):
    
    ### Get Headers ###
    headers = request.headers
    user, error = await get_user(headers, db, True)

    if error:
        return custom_response(status_code=401, message=error)

    return custom_response(status_code=200, message="Account information", data={
        "user": user
    })
