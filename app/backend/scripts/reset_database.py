########## Modules ##########
from db.database import Base, engine
from sqlalchemy.exc import SQLAlchemyError

########## Modules ##########
def reset_database():
    try:
        print("[+] Deleting tables...")
        Base.metadata.drop_all(bind=engine)

        print("[+] Creating tables...")
        Base.metadata.create_all(bind=engine)

        return True
    except SQLAlchemyError as e:
        print(f"[-] Error: {e}")
        return False
