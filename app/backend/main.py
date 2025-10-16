########## Modules ##########
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import Base, engine, SessionLocal

from routes import test
from routes.public import users, videos
from routes.private import accounts, channels, studio, ai
from scripts.init_email_domains import init_email_domains

from services.smtp.main import send_mail_worker
from services.ai.main import Autonomous_Agent

########## Create tables ##########
Base.metadata.create_all(bind=engine)

########## Initializations ##########
app = FastAPI(
    title = "Floua app",
    description = "Backend",
    version = "1.0.0",
)

ai_agent = Autonomous_Agent()

########## Events ##########
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_email_domains(db)

        ### Workers ###
        asyncio.create_task(send_mail_worker())
    finally:
        db.close()


########## CORS ##########
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://192.168.1.74:3000", "http://192.168.1.74:3002", "http://192.168.1.74:3003"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## Routes ##########
app.include_router(test.router)

########## API Routes ##########
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["Accounts"])
app.include_router(channels.router, prefix="/api/channels", tags=["Channels"])
app.include_router(studio.router, prefix="/api/studio", tags=["Studio"])
app.include_router(videos.router, prefix="/api/videos", tags=["Videos"])
app.include_router(ai.router, prefix="/api/ai", tags=["Ai"])
