########## Modules ##########
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import Base, engine
from db.models import User, User_Session, Video, Comments, Video_Playlist, Playlist

from routes import test

########## Create tables ##########
Base.metadata.create_all(bind=engine)

########## Init app ##########
app = FastAPI(
    title = "Floua app",
    description = "Backend",
    version = "1.0.0",
)

########## CORS ##########
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## Routes ##########
app.include_router(test.router)