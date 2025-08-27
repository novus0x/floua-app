########## Modules ##########
from pydantic_settings import BaseSettings

########## Settings ##########
class Settings(BaseSettings):
    SECRET_KEY: str
    CDN_ORIGIN: str
    BACKEND_ORIGIN: str
    MEDIA_ORIGIN: str
    PORT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    WASABI_BUCKET_NAME: str
    WASABI_ACCESS_KEY: str
    WASABI_SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
