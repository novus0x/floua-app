########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

##### Playlist #####
class Video_Playlist(Base):
    __tablename__ = "video_playlist"

    playlist_id = Column(String, ForeignKey("playlists.id"), primary_key=True)
    video_id = Column(String, ForeignKey("videos.id"), primary_key=True)
    position = Column(Integer, nullable=False)

    ## Relationships ##
    video = relationship("Video", back_populates="video_playlists")
    playlist = relationship("Playlist", back_populates="video_playlists")
    
class Playlist_Visibility(str, enum.Enum):
    public = "public"
    private = "private"
    unlisted = "unlisted"

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    visibility = Column(Enum(Playlist_Visibility), default=Playlist_Visibility.public)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    ## Relationships ##
    user = relationship("User", back_populates="playlists")
    video_playlists = relationship("Video_Playlist", back_populates="playlist", cascade="all, delete-orphan")
