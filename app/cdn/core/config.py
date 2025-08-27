########## Modules ##########
from pydantic_settings import BaseSettings

########## Settings ##########
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    BACKEND_ORIGIN: str
    NODE_ORIGIN: str
    MEDIA_ORIGIN: str
    UPLOAD_EXPIRE_MINUTES: int
    STREAM_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    WASABI_BUCKET_NAME: str
    WASABI_ACCESS_KEY: str
    WASABI_SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()