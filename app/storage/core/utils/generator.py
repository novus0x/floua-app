########## Modules ##########
import os, hmac, hashlib, base64, uuid

from sqlalchemy.orm import Session

from types import SimpleNamespace

from core.config import settings

########## Get uuid v4 ##########
async def get_uuid(model, db: Session):
    uid = str(uuid.uuid4())

    while (1):
        if db.query(model).filter(model.id == uid).first():
            uid = str(uuid.uuid4())
        else: break
    
    return uid

########## Generate signature ##########
def generate_signature(path: str, expires: int):
    message = f"{path}{expires}".encode("utf-8")
    signature = hmac.new(settings.SECRET_KEY.encode("utf-8"), message, hashlib.sha256).digest()
    signed = base64.urlsafe_b64encode(signature).decode("utf-8")
    return signed

########## Build signed url ##########
def build_signed_url(base_url: str, path: str, expires: int):
    signature = generate_signature(path, expires)
    url_signed =  f"{base_url}/{path}?expires={expires}&signature={signature}"
    return url_signed
