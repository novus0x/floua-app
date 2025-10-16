########## Modules ##########
from sqlalchemy.orm import Session

from typing import Dict, List, Optional

from db.model import User, Conversation_Memory, Knowledge_Base_Official, Teaching_Proposal, Chat_Session

from services.ai.core.reasoning import Reasoning
from services.ai.core.context_manager import Context_Manager
from services.ai.core.approval_system import Approval_System
from services.ai.core.learning import Autonomous_Learning
from services.ai.core.teaching import Controlled_Teaching_Interface
from services.ai.core.functions import Function_Caller
from services.ai.core.personalization import Personalization
from services.ai.core.chat_manager import Chat_Manager

from core.utils.db_management import add_db

########## Autonomous Agent ##########
class Autonomous_Agent:
    def __init__(self):
        self.chat_manager = Chat_Manager()
        self.reasoning_engine = Reasoning()
        self.approval_system = Approval_System()
        self.context_manager = Context_Manager()
        self.function_caller = Function_Caller()
        self.learning_engine = Autonomous_Learning()
        self.personalization_engine = Personalization()
        self.teaching_interfacte = Controlled_Teaching_Interface()

        self._register_available_functions()

        self.current_state = {
            "primary_language": "en",
            "learning_mode": "active",
            "focus_domains": ["general_knowledge"],
            "confidence": 0.3
        }

    def _register_available_functions(self):
        # self.function_caller.register_function()
        return None

    def process_interaction(self, db: Session, user_input: str, user: User):
        if user_input.startswith("/teach"):
            return self.teaching_interfacte.process_teaching_command(db, user_input, user)
        elif user_input.startswith("/customize"):
            return self._process_customization_command(db, user_input, user)
        elif user_input.startswith("/feedback"):
            return self._process_feedback_command(db, user_input, user)
        elif user_input.startswith("/function"):
            return self._process_function_call(db, user_input, user)
        
        context = self.context_manager.get_conversation_context(db, user)
        english_input = self._ensure_english(user_input)

        learning_result = self.learning_engine.process_learning_experience(db, english_input, "user_interaction", user)
        official_knowledge = self._search_official_knowledge(db, english_input)

        reasoning_result = self.reasoning_engine.reason_about_query(db, english_input, {
            "official_knowledge": official_knowledge,
            "conversation_context": context,
            "user_id": user.id
        })

        response = self._generate_response(reasoning_result, learning_result, official_knowledge)
        customization = self.personalization_engine.get_user_customization(db, user)
        personalized_response = self.personalization_engine.apply_personalization(response, customization, {"context": context})

        analysis = {
            "intent": reasoning_result.get("reasoning_method"),
            "topics": learning_result.get("concepts_learned", [])[:3] if learning_result.get("success", True) else [],
            "response_topics": learning_result.get("concepts_learned", [])[:2] if learning_result.get("success", True) else []
        }

        self.context_manager.update_conversation_context(db, user, user_input, personalized_response, analysis)

        return {
            "success": True,
            "response": personalized_response,
            "language": "en",
            "learning_outcome": learning_result,
            "reasoning_process": reasoning_result,
            "used_official_knowledge": bool(official_knowledge),
            "personalization_applied": True,
            "conversation_context_used": len(context)
        }

    def _process_customization_command(self, db: Session, command: str, user):
        parts = command.replace("/customize", "").strip().split()
        updates = {}

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)

                if key in ["humor_level", "formality_level"]:
                    value = int(value)
                elif key in ["proactive_learning", "ask_clarifying_question"]:
                    value = value.lower() == "true"
                
                updates[key] = value

        return self.personalization_engine.update_customization(db, user, updates)

    def _process_feedback_command(self, db: Session, command: str, user):
        feedback_text = command.replace("/feedback", "").strip()

        new_feedback_entry = Conversation_Memory(
            user_id = user.id,
            message_content = feedback_text,
            message_type = "feedback",
            sentiment = 0.0,
            user_feedback = {
                "type": "explicit_feedback",
                "content": feedback_text
            }
        )

        add_db(db, new_feedback_entry)

        return {
            "success": True,
            "message": "Thank you for your feedback! This helps me learn and improve."
        }

    def _process_function_call(self, db: Session, command: str, user):
        parts = command.replace("/function", "").strip().split()
        function_name = parts[0] if parts else ""

        params = {}

        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=", 1)
                value = value.strip('"\'')

                if value.isdigit():
                    value = int(value)
                elif value.replace(".", "").isdigit():
                    value = float(value)

                params[key] = values

        return self.function_caller.call_function(db, function_name, params, user)

    def _ensure_english(self, text: str):
        ### Future
        return text

    def _search_official_knowledge(self, db: Session, query: str):
        knowledge = db.query(Knowledge_Base_Official).filter(
            Knowledge_Base_Official.language == "en"
        ).first()

        if knowledge:
            return {
                "question": knowledge.question,
                "answer": knowledge.answer,
                "confidence": knowledge.confidence_score
            }
        
        return None

    def _generate_response(self, reasoning_result: Dict, learning_result: Dict, official_knowledge: Optional[Dict]):
        if official_knowledge and official_knowledge["confidence"] > 0.7:
            response = official_knowledge["answer"]
            response += "\n\n(This is approved knowledge from our database)"
        elif reasoning_result["conclusion"]:
            response = reasoning_result["conclusion"]

            if reasoning_result["confidence"] < 0.5:
                response += "\n\nI'm still learning about this. Could you provide more details?"
        
        else:
            response = "I'm processing this information and learning from it."
            response += " Could you help me understand better by providing more context?"

            if learning_result.get("success", True) and learning_result.get("concepts_learned"):
                concepts = [concept["concept"] for concept in learning_result["concepts_learned"][:3]]
                response += f"\n\nI'm learning about: {', '.join(concepts)}"
        
        return response

    def get_user_conversation_history(self, db: Session, user: User):
        conversation = self.context_manager.get_user_conversation(db, user)

        return {
            "success": True,
            "user_id": user.id,
            "total_messages": conversation.total_messages,
            "last_active": conversation.last_active,
            "current_topic": conversation.current_topic,
            "conversation_history": conversation.conversation_history,
            "user_preferences": conversation.user_preferences
        }

    def get_approval_queue(self, db: Session, user: User):
        pending_proposal = self.approval_system.get_pending_proposal(db)

        return {
            "success": True,
            "pending_count": len(pending_proposal),
            "proposal": pending_proposal
        }

    def review_teaching_proposal(self, db: Session, proposal: Teaching_Proposal, user: User, review_data: Dict):
        return self.approval_system.review_proposal(db, proposal, user, review_data)

    def create_chat_session(self, db: Session, user: User, title: str = "New Chat"):
        return self.chat_manager.create_chat_session(db, user, title)

    def get_chat_session(self, db: Session, chat: Chat_Session, user: User):
        return self.chat_manager.get_chat_session(db, chat, user)

    def get_chat_messages(self, db: Session, chat: Chat_Session, user: User, start: int = 1, finish: int = 50):
        return self.chat_manager.get_chat_messages(db, chat, user, start, finish)

    def add_chat_message(self, db: Session, chat: Chat_Session, user: User, message_type: str, content: str, ai_metadata: Dict = None):
        return self.chat_manager.add_message_to_chat(db, chat, user, message_type, content, ai_metadata)

    def deactive_chat_session(self, db: Session, chat: Chat_Session, user: User):
        return self.chat_manager.soft_delete_chat_session(db, chat, user)

    def edit_chat_title(self, db: Session, chat: Chat_Session, user: User, new_title: str):
        return self.chat_manager.edit_chat_title(db, chat, user, new_title)

    def get_user_chat_sessions(self, db: Session, user: User):
        return self.chat_manager.get_user_chat_sessions(db, user)

    def get_active_chat_sessions(self, db: Session, user: User):
        return self.chat_manager.get_active_chat_sessions(db, user)

    def soft_delete_chat_session(self, db: Session, chat: Chat_Session, user: User):
        return self.chat_manager.soft_delete_chat_session(db, chat, user)
