########## Modules ##########
import re, json

from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from db.model import User, User_Conversation, Conversation_Memory

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Context Manager ##########
class Context_Manager:
    def __init__(self):
        self.max_context_length = 25

    def get_user_conversation(self, db: Session, user: User) -> User_Conversation:
        conversation = db.query(User_Conversation).filter(
            User_Conversation.user_id == user.id
        ).first()

        if not conversation:
            new_conversation = User_Conversation(
                id = get_uuid(User_Conversation, db),
                user_id = user.id,
                conversation_history = [],
                user_preferences = {}
            )

            add_db(db, new_conversation)

        return conversation
    
    def update_conversation_context(self, db: Session, user: User, user_message: str, ai_response: str, analysis: Dict) -> User_Conversation:
        conversation = self.get_user_conversation(db, user)

        user_message_entry = {
            "type": "user",
            "content": user_message,
            "timestamp": datetime.utcnow().isoformat(),
            "intent": analysis.get("intent"),
            "topics": analysis.get("topics", [])
        }

        ai_message_entry = {
            "type": "assistant",
            "content": ai_response,
            "timestamp": datetime.utcnow().isoformat(),
            "topics": analysis.get("response_topics", [])
        }

        current_history = conversation.conversation_history or []
        current_history.extend([user_message_entry, ai_message_entry])
        conversation.conversation_history = current_history[-self.max_context_length * 2:]

        if analysis.get("topics"):
            conversation.current_topic = analysis["topics"][0]

        conversation.total_messages += 2
        conversation.last_active = datetime.utcnow()

        return conversation

    def get_conversation_context(self, db: Session, user: User):
        conversation = self.get_user_conversation(db, user)

        return conversation.conversation_history or []

    def learn_user_preferences(self, db: Session, user: User, message: str, analysis: Dict, user_feedback: Dict = None):
        conversation = self.get_conversation(db, user)

        if analysis.get("topics"):
            current_prefs = conversation.user_preferences or {}
            topics_prefs = current_prefs.get("topics", {})

            for topic in analysis["topics"]:
                topics_prefs[topic] = topics_prefs.get(topic, 0) + 1
            
            current_prefs["topics"] = topics_prefs
            conversation.user_preferences = current_prefs
        
        if user_feedback:
            self._process_user_feedback(db, user, user_feedback)
    
    def _process_user_feedback(self, db: Session, user: User, feedback: Dict):
        new_feedback_entry = Conversation_Memory(
            id = get_uuid(Conversation_Memory, db),
            user_id = user.id,
            message_content = feedback.get("sentiment", 0.0),
            user_feedback = feedback
        )

        add_db(db, new_feedback_entry)
