########## Modules ##########
import enum
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, LargeBinary, JSON, Enum

from db.database import Base

##########  ##########
class Chat_Message_Type(enum.Enum):
    user = "user"
    assistant = "assistant"

########## Chat Session ##########
class Chat_Session(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    title = Column(String(250), default="New Chat")
    is_active = Column(Boolean, default=True)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("Chat_Message", back_populates="chat_session", cascade="all, delete-orphan")

########## Chat Message ##########
class Chat_Message(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, nullable=False, index=True)
    chat_session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)

    message_type = Column(Enum(Chat_Message_Type), default=Chat_Message_Type.user)
    content = Column(Text, nullable=False)
    language = Column(String(50), default="en")

    reasoning_data = Column(JSON)
    knowledge_used = Column(JSON)
    personalization_applied = Column(Boolean, default=False)

    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    chat_session = relationship("Chat_Session", back_populates="messages")
