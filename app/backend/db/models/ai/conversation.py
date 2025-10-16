########## Modules ##########
import enum

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, LargeBinary, JSON, Enum

from db.database import Base

########## User Conversation ##########
class User_Conversation(Base):
    __tablename__ = "user_conversations"

    id = Column(String, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    ai_personality = Column(String(250), default="neutral")
    preferred_tone = Column(String(250), default="balanced")

    learning_focus = Column(JSON)
    language_preference = Column(String(50), default="en")

    current_topic = Column(String(250))
    conversation_history = Column(JSON)
    user_preferences = Column(JSON)
    total_messages = Column(Integer, default=0)
    
    last_active = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="conversations")

########## User Conversation ##########
class Conversation_Memory(Base):
    __tablename__ = "conversation_memories"

    id = Column(String, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String, ForeignKey("user_conversations.id"))
    
    message_content = Column(Text)
    message_type = Column(String(50))
    
    detected_intent = Column(String(250))
    entities_mentioned = Column(JSON)
    sentiment = Column(Float)
    topics = Column(JSON)

    context_data = Column(JSON)
    user_feedback = Column(JSON)

    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    conversation = relationship("User_Conversation")
    user = relationship("User", back_populates="conversation_memories")

class User_AI_Customization(Base):
    __tablename__ = "user_ai_customizations"

    id = Column(String, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    custom_name = Column(String(250), default="Assistant")
    response_style = Column(String(250), default="balanced")
    humor_level = Column(Integer, default=0)
    formality_level = Column(Integer, default=2)

    preferred_domains = Column(JSON)
    expertise_level = Column(String(50), default="beginner")

    proactive_learning = Column(Boolean, default=True)
    ask_clarifying_questions = Column(Boolean, default=True)
    share_learning_process = Column(Boolean, default=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ## Relationships ##
    user = relationship("User", back_populates="ai_customization")
