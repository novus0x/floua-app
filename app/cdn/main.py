########## Modules ##########
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import Base, engine, SessionLocal

from routes import videos

########## Create tables ##########
Base.metadata.create_all(bind=engine)

########## Init app ##########
app = FastAPI(
    title = "Floua CDN",
    description = "CDN",
    version = "1.0.0",
)

########## CORS ##########
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## API Routes ##########
app.include_router(videos.router, prefix="/videos", tags=["Videos"])
