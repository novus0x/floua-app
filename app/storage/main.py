########## Modules ##########
import asyncio

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.utils.converter import video_converter

from routes import videos

########## Variables ##########
SAVE_DIR = Path("videos").absolute()

########## Init app ##########
app = FastAPI(
    title = "Floua Node",
    description = "Node 1",
    version = "1.0.0",
)

########## Events ##########
@app.on_event("startup")
def startup_event():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # Task converter
    app.state.converter_task = asyncio.create_task(video_converter())
    app.state.SAVE_DIR = SAVE_DIR

########## CORS ##########
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["192.168.1.80:3002"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## API Routes ##########
app.include_router(videos.router, prefix="/videos", tags=["Videos"])
