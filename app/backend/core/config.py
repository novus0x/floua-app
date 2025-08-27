########## Modules ##########
from pydantic_settings import BaseSettings

########## Settings ##########
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    FRONTEND_ORIGIN: str
    CDN_ORIGIN: str
    TOKEN_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    EMAIL_HOST: str
    EMAIL_PORT: int

    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()