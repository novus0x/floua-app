########## Modules ##########
from pydantic_settings import BaseSettings

########## Settings ##########
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CDN_ORIGIN: str
    PORT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

settings = Settings()
