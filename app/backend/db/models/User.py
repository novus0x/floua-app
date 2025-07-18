########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### User #####
class User_Role(str, enum.Enum):
    viewer = "viewer"
    creator = "creator"
    company = "company"
    moderator = "moderator"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    birth = Column(DateTime, nullable=False)

    email_verified = Column(Boolean, default=False)
    user_session_extra = Column(Boolean, default=False)

    display_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    points = Column(Integer, default=0)
    role = Column(Enum(User_Role), default=User_Role.viewer)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    videos = relationship("Video", back_populates="user")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("User_Session", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Point_Transaction", back_populates="user", cascade="all, delete-orphan")
    external_accounts = relationship("External_Account", back_populates="user", cascade="all, delete-orphan")

##### User Sessions #####
class User_Session(Base):
    __tablename__ = "user_session"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

    ip_addr = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    location = Column(String, nullable=True)
    device_name = Column(String, nullable=True)

    last_used_at = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="sessions")

##### External Accounts #####
class OAuth_Provider(str, enum.Enum):
    google = "google"
    tidal = "tidal"

class External_Account(Base):
    __tablename__ = "external_accounts"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    email = Column(String, nullable=True)
    
    provider = Column(Enum(OAuth_Provider), nullable=False)
    external_id = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="external_accounts")
