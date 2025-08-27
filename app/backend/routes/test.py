########## Modules ##########
from fastapi import APIRouter
from scripts.reset_database import reset_database

from db.database import Base, engine, SessionLocal

from scripts.init_email_domains import init_email_domains

########## Variables ##########
router = APIRouter()

########## Reset DB ##########
@router.get("/reset-db")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    success = reset_database()

    if not success:
        raise HTTPException(status_code=500, detail="Database reset failed")

    db = SessionLocal()
    try:
        init_email_domains(db)
    finally:
        db.close()

    return {"status": "success", "message": "Database reset and initialized"}
