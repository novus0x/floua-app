########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### Video #####
class Video_Status(str, enum.Enum):
    error = "error"
    uploading = "uploading"
    upload = "upload"
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

class Video_Point_Stats(Base):
    __tablename__ = "video_point_stats"

    id = Column(String, primary_key=True, nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)

    total_points = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    video = relationship("Video")

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, nullable=False)
    short_id = Column(String(12), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Video_Status), default=Video_Status.uploading)
    visibility = Column(Enum(Video_Visibility), default=Video_Visibility.public)
    
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    source_type = Column(Enum(Video_Source_type), default=Video_Source_type.cdn)
    source_url = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="videos")
    comments = relationship("Comment", back_populates="video", cascade="all, delete-orphan")
    video_playlists = relationship("Video_Playlist", back_populates="video", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="videos")

