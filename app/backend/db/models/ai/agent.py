########## Modules ##########
import enum

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, LargeBinary, JSON, Enum

from db.database import Base

##########  ##########
class Learning_Strategy(enum.Enum):
    active = "active"
    passive = "passive"
    exploratory = "exploratory"
    focused = "focused"

class Knowledge_Source(enum.Enum):
    user_interaction = "user_interaction"
    document_analysis = "document_analysis"
    conversation_pattern = "conversation_pattern"
    feedback_analysis = "feedback_analysis"
    self_reflection = "self_reflection"
    external_api = "external_api"

########## Agent Memory ##########
class Agent_Memory(Base):
    __tablename__ = "agent_memory"

    id = Column(String, primary_key=True, nullable=False, index=True)

    experience_type = Column(String(50))
    content = Column(Text)
    context = Column(JSON)
    emotional_weight = Column(Float, default=0.0)

    concepts_learned = Column(JSON)
    patterns_recognized = Column(JSON)
    relationships = Column(JSON)

    confidence_level = Column(Float, default=0.0)
    verification_count  = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date = Column(DateTime, default=datetime.utcnow)

########## Learning Experience ##########
class Learning_Experience(Base):
    __tablename__ = "learning_experiences"

    id = Column(String, primary_key=True, nullable=False, index=True)
    
    input_data = Column(Text, nullable=False)
    input_type = Column(String(250))
    source = Column(String(250))

    learning_strategy = Column(Enum(Learning_Strategy), default=Learning_Strategy.passive)
    concepts_extracted = Column(JSON)
    knowledge_gaps_found = Column(JSON)

    new_knowledge_created = Column(Boolean, default=False)
    knowledge_verified = Column(Boolean, default=False)
    confidence_gain = Column(Float, default=0.0)
    processing_time = Column(Float)
    
    date = Column(DateTime, default=datetime.utcnow)

########## Concept Network ##########
class Concept_Network(Base):
    __tablename__ = "concept_network"

    id = Column(String, primary_key=True, nullable=False, index=True)

    concept_name = Column(String(250), nullable=False, index=True)
    concept_definition = Column(Text)
    language = Column(String(50), default="en")

    abstraction_level = Column(Integer, default=1)
    domain = Column(String(250))
    complexity = Column(Float, default=0.0)

    related_concepts = Column(JSON)
    prerequisites = Column(JSON)
    applications = Column(JSON)

    usage_frequency = Column(Integer, default=1)
    last_used = Column(DateTime, default=datetime.utcnow)

    confidence = Column(Float, default=0.0)
    learned_from = Column(JSON)

    date = Column(DateTime, default=datetime.utcnow)

########## Reasoning Pattern ##########
class Reasoning_Pattern(Base):
    __tablename__ = "reasoning_patterns"

    id = Column(String, primary_key=True, nullable=False, index=True)

    pattern_name = Column(String(250))
    pattern_type = Column(String(250))
    description = Column(Text)

    input_examples = Column(JSON)
    output_examples = Column(JSON)
    success_criteria = Column(JSON)

    applicable_domains = Column(JSON)
    confidence_threshold = Column(Float, default=0.7)

    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    last_used = Column(DateTime, default=datetime.utcnow)

########## Language Model ##########
class Language_Model(Base):
    __tablename__ = "language_models"
    
    id = Column(String, primary_key=True, nullable=False, index=True)
    
    language_code = Column(String(10), nullable=False, index=True)
    language_name = Column(String(50))

    vocabulary = Column(JSON)
    grammar_patterns = Column(JSON)
    common_phrases = Column(JSON)

    word_count = Column(Integer, default=0)
    phrases_count = Column(Integer, default=0)
    fluency_score = Column(Float, default=0.0)

    learning_progress = Column(Float, default=0.0)
    last_learning_session = Column(DateTime)
    
    date = Column(DateTime, default=datetime.utcnow)

########## Agent State ##########
class Agent_State(Base):
    __tablename__ = "agent_states"

    id = Column(String, primary_key=True, nullable=False, index=True)

    current_focus = Column(String(250))
    learning_priority = Column(JSON)
    active_goals = Column(JSON)

    knowledge_domains = Column(JSON)
    language_abilities = Column(JSON)
    reasoning_capabilities = Column(JSON)

    confidence_level = Column(Float, default=0.5)
    curiosity_level = Column(Float, default=0.8)
    learning_speed = Column(Float, default=1.0)

    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_learning_experiences = Column(Integer, default=0)

########## Self Reflection ##########
class Self_Reflection(Base):
    __tablename__ = "self_reflections"

    id = Column(String, primary_key=True, nullable=False, index=True)

    reflection_type = Column(String(250))
    trigger_event = Column(Text)

    strengths_identified = Column(JSON)
    weaknesses_identified = Column(JSON)
    knowledge_gaps_found = Column(JSON)
    improvement_ideas = Column(JSON)

    action_plan = Column(JSON)
    learning_goals = Column(JSON)

    improvements_made = Column(JSON)
    effectiveness_score = Column(Float, default=0.0)

    date = Column(DateTime, default=datetime.utcnow)

########## Learning Goal ##########
class Learning_Goal(Base):
    __tablename__ = "learning_goals"
    
    id = Column(String, primary_key=True, nullable=False, index=True)
    
    goal_description = Column(Text, nullable=False)
    goal_type = Column(String(250))
    priority_level = Column(Integer, default=1)

    target_metrics = Column(JSON)
    prerequisites = Column(JSON)
    resources_needed = Column(JSON)

    current_progress = Column(Float, default=0.0)
    milestone = Column(JSON)
    completed = Column(JSON)

    current_progress = Column(Float, default=0.0)
    milestones = Column(JSON)
    completed = Column(Boolean, default=False)

    date = Column(DateTime, default=datetime.utcnow)
    target_completion = Column(DateTime)
    completed_at = Column(DateTime)
