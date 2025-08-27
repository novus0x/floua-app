########## Modules ##########
from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from core.config import settings

########## Variables ##########
# DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"

########## Engine ##########
engine = create_engine(settings.DATABASE_URL, future=True)

########## Create Session ##########
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

##########  Base ##########
Base = declarative_base()

########## Get DB Session ##########
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
