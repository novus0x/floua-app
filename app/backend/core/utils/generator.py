########## Modules ##########
import json, uuid, random, string, time

from sqlalchemy.orm import Session

from types import SimpleNamespace

from core.config import settings

########## Get uuid v4 ##########
def get_uuid(model, db: Session):
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

