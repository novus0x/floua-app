########## Modules ##########
import bcrypt

from core.config import settings

########## Hash password ##########
def hash_token(token):
    salt = bcrypt.gensalt()
    hashed_token = bcrypt.hashpw(token.encode("utf-8"), salt)

    return hashed_token.decode("utf-8")

########## Check password ##########
def check_token(encrypted_token, token):
    return bcrypt.checkpw(token.encode("utf-8"), encrypted_token.encode("utf-8"))
