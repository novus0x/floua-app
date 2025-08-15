########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### Poinst #####
class Point_Transaction_Type(str, enum.Enum):
    earn = "earn"
    spend = "spend"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"

class Point_Transaction(Base):
    __tablename__ = "point_transactions"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=True)  # opcional si está relacionado a un video

    amount = Column(Integer, nullable=False)
    type = Column(Enum(Point_Transaction_Type), nullable=False)
    description = Column(Text, nullable=True)

    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User")
    video = relationship("Video")