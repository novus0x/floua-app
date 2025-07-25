########## Modules ##########
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import Base, engine, SessionLocal

from routes import videos, nodes

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
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## API Routes ##########
app.include_router(videos.router, prefix="/videos", tags=["Videos"])

########## WebSocket Routes ##########
app.mount("/nodes", nodes.router)
app.mount("/ws", nodes.router_ws)
