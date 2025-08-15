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
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    birth = Column(DateTime, nullable=False)

    email_verified = Column(Boolean, default=False)
    has_channel = Column(Boolean, default=False)
    user_session_extra = Column(Boolean, default=True)

    bio = Column(Text, nullable=True)
    avatar_url = Column(String, default="/img/default_avatar.png")

    points = Column(Integer, default=0)
    role = Column(Enum(User_Role), default=User_Role.viewer)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    verification = relationship("User_Verification", back_populates="user")
    channel = relationship("User_Channel", back_populates="user")
    follow = relationship("User_Follow", back_populates="user")
    videos = relationship("Video", back_populates="user")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("User_Session", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Point_Transaction", back_populates="user", cascade="all, delete-orphan")
    external_accounts = relationship("External_Account", back_populates="user", cascade="all, delete-orphan")

##### User Verification #####
class User_Verification(Base):
    __tablename__ = "user_verification"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="verification")

##### User Sessions #####
class User_Session(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    ip_addr = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    location = Column(String, nullable=True)

    last_used_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="sessions")

##### User Channel #####
class User_Channel(Base):
    __tablename__ = "user_channels"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    tag = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    avatar_url = Column(String, default="/img/default_avatar.png")

    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="channel")
    follow = relationship("User_Follow", back_populates="channel")
    videos = relationship("Video", back_populates="channel")

##### User Follows #####
class User_Follow(Base):
    __tablename__ = "user_follows"

    id = Column(String, primary_key=True, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    channel_id = Column(String, ForeignKey("user_channels.id"), nullable=False)

    ## Relationships ##
    user = relationship("User", back_populates="follow")
    channel = relationship("User_Channel", back_populates="follow")

##### External Accounts #####
class OAuth_Provider(str, enum.Enum):
    google = "google"
    tidal = "tidal"
    kick = "kick"

class External_Account(Base):
    __tablename__ = "external_accounts"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    email = Column(String, nullable=True)
    
    provider = Column(Enum(OAuth_Provider), nullable=False)
    external_id = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="external_accounts")
