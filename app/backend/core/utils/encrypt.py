########## Modules ##########
import jwt, bcrypt, datetime

from core.config import settings

########## Hash password ##########
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")

########## Check password ##########
def check_password(encrypted_password, password):
    return bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8"))

########## Check JWT ##########
def check_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None, True

    return payload, None

########## Generate JWT ##########
def generate_jwt(session_id, expires):
    payload = {"session_id": session_id}

    if expires == "1":
        payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return encoded_jwt
