########## Modules ##########
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

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