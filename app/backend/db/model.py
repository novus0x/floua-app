########## Modules ##########
import enum, uuid

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean

from db.models.User import User, User_Session, External_Account, User_Channel, User_Follow, User_Role, User_Verification
from db.models.Point import Point_Transaction

from db.models.Playlist import Playlist, Video_Playlist
from db.models.Video import Video

##### Category #####
class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    ## Relationships ##
    videos = relationship("Video", back_populates="category")

##### Allowed Email Domain #####
class Allowed_Email_Domain(Base):
    __tablename__ = "allowed_email_domains"

    domain = Column(String, primary_key=True)
    description = Column(String, nullable=True)

##### Comments #####
class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    parent_id = Column(String, ForeignKey("comments.id"), nullable=True)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    ## Relationships ##
    user = relationship("User", back_populates="comments")
    video = relationship("Video", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")

##### History #####
class Watch_History(Base):
    __tablename__ = "watch_history"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    progress = Column(Integer, default=0)

    watched_at = Column(DateTime(timezone=True), default=datetime.utcnow)

##### Notification #####
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User")
