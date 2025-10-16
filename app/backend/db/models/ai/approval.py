########## Modules ##########
import enum

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, LargeBinary, JSON, Enum

from db.database import Base

##########  ##########
class Approval_Status(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    needs_revision = "needs_revision"

########## Teaching Proposal ##########
class Teaching_Proposal(Base):
    __tablename__ = "teaching_proposals"

    id = Column(String, primary_key=True, nullable=False, index=True)

    proposed_by_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    language = Column(String(50), default="en")
    context_examples = Column(JSON)
    proposed_category = Column(String(250))

    teaching_method = Column(String(250))
    complexity_level = Column(Integer, default=1)
    source_reliability = Column(Float, default=0.5)

    user_expertise = Column(Float, default=0.0)

    status = Column(Enum(Approval_Status), default=Approval_Status.pending, index=True)
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)

    moderator_notes = Column(Text)
    confidence_score = Column(Float, default=0.0)
    needs_verification = Column(Boolean, default=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

    ## Relationships ##
    proposed_by_user = relationship("User", back_populates="teaching_proposals", foreign_keys=[proposed_by_user_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by_user_id])
    
    reviews = relationship("Proposal_Review", back_populates="proposal")

########## Proposal Review ##########
class Proposal_Review(Base):
    __tablename__ = "proposal_reviews"

    id = Column(String, primary_key=True, nullable=False, index=True)
    proposal_id = Column(String, ForeignKey("teaching_proposals.id"), nullable=False)
    reviewed_by_user_id = Column(String, ForeignKey("users.id"), nullable=False)

    accuracy_score = Column(Float)
    clarity_score = Column(Float)
    relevance_score = Column(Float)
    overall_score = Column(Float)

    strengths = Column(JSON)
    weaknesses = Column(JSON)
    suggestions = Column(JSON)

    recommendation = Column(String(250))
    decision = Column(String(250))

    date = Column(DateTime, default=datetime.utcnow)
    
    ## Relationships ##
    proposal = relationship("Teaching_Proposal", back_populates="reviews")
    reviewed_by_user = relationship("User", back_populates="proposal_reviews", foreign_keys=[reviewed_by_user_id])

class Knowledge_Base_Official(Base):
    __tablename__ = "knowledge_base_official"

    id = Column(String, primary_key=True, nullable=False, index=True)

    question = Column(Text, nullable=False, index=True)
    answer = Column(Text, nullable=False)
    language = Column(String(50), default="en", index=True)

    domain = Column(String(250), index=True)
    category = Column(String(250))
    tags = Column(JSON)

    confidence_score = Column(Float, default=0.0)
    verification_count = Column(Integer, default=0)
    usage_count = Column(Integer, default=0)

    source_proposal_id = Column(String, ForeignKey("teaching_proposals.id"))
    added_by_user_id = Column(String, ForeignKey("users.id"), nullable=False)

    last_verified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)
    
    ## Relationships ##
    source_proposal = relationship("Teaching_Proposal")    
    added_by_user = relationship("User", foreign_keys=[added_by_user_id])
