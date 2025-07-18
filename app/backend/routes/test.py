########## Modules ##########
from fastapi import APIRouter
from scripts.reset_database import reset_database

########## Variables ##########
router = APIRouter()

########## Reset DB ##########
@router.get("/reset-db")
def reset_db():
    success = reset_database()

    if not success:
        raise HTTPException(status_code=500, detail="Database reset failed")

    db = SessionLocal()
    try:
        init_email_domains(db)
    finally:
        db.close()

    return {"status": "success", "message": "Database reset and initialized"}
