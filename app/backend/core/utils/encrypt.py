########## Modules ##########
import jwt, bcrypt, datetime, time

from core.config import settings


########## Hash password ##########
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")

########## Check password ##########
def check_password(encrypted_password, password):
    return bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8"))

########## Generate JWT ##########
def generate_jwt(session_id, expires):
    payload = {"session_id": session_id, "exp": False}

    if expires == "1":
        payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return encoded_jwt
