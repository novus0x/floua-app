########## Modules ##########
from sqlalchemy.orm import Session
from db.model import Allowed_Email_Domain

##### Variables #####
initial_domains = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "icloud.com",
    "protonmail.com"
]

##### Actions #####
def init_email_domains(db: Session):
    for domain in initial_domains:
        exists = db.query(Allowed_Email_Domain).filter_by(domain=domain).first()
        if not exists:
            db.add(Allowed_Email_Domain(domain=domain))
    db.commit()
