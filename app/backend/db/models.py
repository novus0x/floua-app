########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### User #####
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    videos = relationship("Video", back_populates="user")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("User_Session", back_populates="user", cascade="all, delete-orphan")

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
    last_used_at = Column(DateTime, nullable=True)
    
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="sessions")

##### Video #####
class Video_Status(str, enum.Enum):
    error = "error"
    uploading = "uploading",
    upload = "upload",
    processing = "processing"
    ready = "ready"

class Video_Visibility(str, enum.Enum):
    public = "public"
    private = "private"
    unlisted = "unlisted"

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Video_Status), default=Video_Status.uploading)
    visibility = Column(Enum(Video_Visibility), default=Video_Visibility.public)
    
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    filename = Column(String, nullable=False)
    m3u8_url = Column(String, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="videos")
    comments = relationship("Comment", back_populates="video", cascade="all, delete-orphan")
    video_playlists = relationship("Video_Playlist", back_populates="videos", cascade="all, delete-orphan")

##### Comments #####
class Comments(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    parent_id = Column(String, ForeignKey("comments.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    ## Relationships ##
    user = relationship("User", back_populates="comments")
    video = relationship("Video", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")


##### Playlist #####
class Video_Playlist(Base):
    __tablename__ = "video_playlist"

    playlist_id = Column(String, ForeignKey("playlists.id"), primary_key=True)
    video_id = Column(String, ForeignKey("videos.id"), primary_key=True)
    position = Column(Integer, nullable=False)

    ## Relationships ##
    video = relationship("Video", back_populates="video_playlist")
    playlist = relationship("Playlist", back_populates="video_playlist")
    
class Playlist_Visibility(str, enum.Enum):
    public = "public"
    private = "private"
    unlisted = "unlisted"

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    visibility = Column(Enum(Video_Visibility), default=Video_Visibility.public)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    ## Relationships ##
    user = relationship("User", back_populates="playlists")
    video_playlists = relationship("Video_Playlist", back_populates="playlist", cascade="all, delete-orphan")
