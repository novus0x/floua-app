########## Modules ##########
import random

from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

from db.model import User, User_AI_Customization

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Personalization ##########
class Personalization:
    def __init__(self):
        self.personality_profiles = {
            "friendly": {
                "greeting": "Hey there!",
                "response_style": "warm and engaging",
                "emojis": True,
                "ask_questions": True
            },
            "professional": {
                "greeting": "Hello, how can I assist you today?",
                "response_style": "crear and concise",
                "emojis": False,
                "ask_questions": True
            },
            "casual": {
                "greeting": "Yo! What's up?",
                "response_style": "relaxed and informal",
                "emojis": True,
                "ask_questions": True
            },
            "technical": {
                "greeting": "Ready to assist with technical matterns.",
                "response_style": "detailed and precise",
                "emojis": False,
                "ask_questions": True
            },
            "neutral": {
                "greeting": "Hello, how can I help you?",
                "response_style": "balanced",
                "emojis": False,
                "ask_questions": True
            }
        }

    def get_user_customization(self, db: Session, user: User) -> User_AI_Customization:
        customization = db.query(User_AI_Customization).filter(
            User_AI_Customization.user_id == user.id
        ).first()

        if not customization:
            new_customization = User_AI_Customization(
                user_id = user.id
            )
            add_db(customization)
        
        return customization

    def update_customization(self, db: Session, user: User, updates: Dict):
        customization = self.get_user_customization(db, user)

        for key, value in updates.items():
            if hasattr(customization, key):
                setattr(customization, key, value)

        customization.updated_at = datetime.utcnow()

        return {
            "success": True,
            "message": "Personalization updated"
        }

    def apply_personalization(self, response: str, customization: User_AI_Customization, context: Dict):
        personality = self.personality_profiles.get(customization.ai_personality or "neutral", self.personality_profiles["neutral"])

        if customization.humor_level > 3 and personality.get("emojis", False):
            response = self._add_humor(response)

        if customization.formality_level < 2:
            response = self._make_informal(response)
        elif customization.formality_level > 4:
            response = self._make_informal(response)

        return response

    def _add_humor(self, text):
        humorous_phrases = []

        if random.random() > 0.7:
            text += random.choice(humorous_phrases)
        
        return text

    def _make_informal(self, text: str):
        replacements = {
            "Hello": "Hey",
            "How can I assist you": "What's up",
            "Please": "",
            "Thank you": "Thanks",
            "I am": "I'm",
            "cannot": "can't"
        }

        for formal, informal in replacements.items():
            text = text.replace(formal, informal)

        return text

    def _make_formal(self, text: str):
        replacements = {
            "Hey": "Hello",
            "What's up": "How can I assist you",
            "Thanks": "Thank you",
            "I'm": "I am",
            "can't": "cannot",
        }

        for informal, formal in replacements.items():
            text = text.replace(informal, formal)

        return text
