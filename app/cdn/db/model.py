########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### Allowed Nodes #####
class Allowed_Node(Base):
    __tablename__ = "allowed_nodes"

    id = Column(String, primary_key=True, nullable=False)
    ip = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    date = Column(DateTime, default=datetime.utcnow)

##### Node #####
class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True, nullable=False)
    ip = Column(String, nullable=False)
    port = Column(Integer,nullable=False)
    active = Column(Boolean, default=True)
    videos_quantity = Column(Integer, default=0)

    last_seen = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

##### Video #####
class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

##### Upload Token #####
class Upload_Token(Base):
    __tablename__ = "upload_tokens"

    id = Column(String, primary_key=True, nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    used = Column(Boolean, default=False)
    
    expires_at = Column(DateTime, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
