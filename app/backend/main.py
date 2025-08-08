########## Modules ##########
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import Base, engine, SessionLocal

from routes import test
from routes.public import users
from routes.private import accounts
from scripts.init_email_domains import init_email_domains

########## Create tables ##########
Base.metadata.create_all(bind=engine)

########## Init app ##########
app = FastAPI(
    title = "Floua app",
    description = "Backend",
    version = "1.0.0",
)

########## Events ##########
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_email_domains(db)
    finally:
        db.close()


########## CORS ##########
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://192.168.1.36:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

########## Routes ##########
app.include_router(test.router)

########## API Routes ##########
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["Accounts"])