########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### Video #####
class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
