########## Modules ##########
import json, uuid, random, string

from fastapi import Request
from sqlalchemy.orm import Session

from db.model import Allowed_Email_Domain

from types import SimpleNamespace

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

########## Get uuid v4 ##########
async def get_uuid(model, db: Session):
    uid = str(uuid.uuid4())

    while (1):
        if db.query(model).filter(model.id == uid).first():
            uid = str(uuid.uuid4())
        else: break
    
    return uid

########## Get short id ##########
async def get_short_id(model, db: Session):
    charset = string.ascii_letters + string.digits + "-_"
    short_id = ''.join(random.choices(charset, k=12))

    while (1):
        if db.query(model).filter(model.id == short_id).first():
            short_id = ''.join(random.choices(charset, k=12))
        else: break
    
    return short_id