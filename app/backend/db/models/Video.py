########## Modules ##########
import enum, uuid

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

from db.database import Base

##### Video #####
class Video_Status(str, enum.Enum):
    error = "error"
    uploading = "uploading"
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"

class Video_Visibility(str, enum.Enum):
    public = "public"
    private = "private"
    unlisted = "unlisted"

class Video_Source_type(str, enum.Enum):
    cdn = "cdn"
    youtube = "youtube"
    external = "external"

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, nullable=False)
    short_id = Column(String(12), unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Video_Status), default=Video_Status.uploading)
    visibility = Column(Enum(Video_Visibility), default=Video_Visibility.public)
    
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    source_type = Column(Enum(Video_Source_type), default=Video_Source_type.cdn)
    thumbnail_url = Column(String, nullable=True)

    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    channel_id = Column(String, ForeignKey("user_channels.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="videos")
    channel = relationship("User_Channel", back_populates="videos")
    comments = relationship("Comment", back_populates="video", cascade="all, delete-orphan")
    video_playlists = relationship("Video_Playlist", back_populates="video", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="videos")
    transactions = relationship("Transaction", back_populates="video")
