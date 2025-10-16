########## Modules ##########
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from db.model import User, Chat_Session, Chat_Message, Chat_Message_Type

from core.utils.generator import get_uuid
from core.utils.db_management import add_db, update_db

########## Chat Manager ##########
class Chat_Manager:
    def __init__(self):
        pass

    def create_chat_session(self, db: Session, user: User, title: str = "New Chat"):
        new_chat_session = Chat_Session(
            id = get_uuid(User, db),
            user_id = user.id,
            title = title,
            is_active = True
        )

        add_db(db, new_chat_session)

        return {
            "id": new_chat_session.id,
            "title": new_chat_session.title,
            "is_active": new_chat_session.is_active,
            "message": "New chat created successfully",
            "date": new_chat_session.date
        }

    def get_active_chat_sessions(self, db: Session, user: User):
        sessions = db.query(Chat_Session).filter(
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).order_by(Chat_Session.updated_at.desc()).all()
        
        sessions_data = []

        for session in sessions:
            sessions_data.append({
                "id": session.id,
                "title": session.title,

                "message_count": len(session.messages),
                "last_message": session.messages[-1].content if session.messages else None,
                "last_message_time": session.messages[-1].date if session.messages else session.date,

                "updated_at": session.updated_at,
                "date": session.date
            })

        return sessions_data
    
    def get_chat_session(self, db: Session, chat: Chat_Session, user: User):
        chat_session = db.query(Chat_Session).filter(
            Chat_Session.id == chat.id,
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).first()

        if not chat_session:
            return None

        return {
            "id": chat_session.id,
            "title": chat_session.title,
            "is_active": chat_session.is_active,
            "total_messages": len(chat_session.messages),
            "updated_at": session.updated_at,
            "date": chat_session.date,
        }
    
    def get_chat_messages(self, db: Session, chat: Chat_Session, user: User, start: int = 1, finish: int = 50):
        chat_session = db.query(Chat_Session).filter(
            Chat_Session.id == chat.id,
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).first()

        if not chat_session:
            return {
                "error": "Chat session not found or not active",
                "messages": [],
                "total": 0
            }
        
        total_messages = len(chat_session.messages)
        start_index = max(0, start - 1)
        end_index = min(total_messages, finish)

        messages = db.query(Chat_Message).filter(
            Chat_Message.chat_session_id == chat.id
        ).order_by(Chat_Message.date.desc()).all()

        paginated_messages = [messages][start_index:end_index]

        messages_data = []

        for message in messages:
            messages_data.append({
                "id": message.id,
                "type": message.message_type,
                "content": message.content,
                "language": message.language,
                "reasoning_data": message.reasoning_data,
                "knowledge_used": message.knowledge_used,
                "personalization_applied": message.personalization_applied,
                "date": message.date,
            })

        return {
            "chat_id": chat.id,
            "title": chat.title,
            "messages": messages_data,
            "pagination": {
                "start": start,
                "finish": end_index,
                "total_messages": total_messages,
                "has_previous": start > 1,
                "has_next": end_index < total_messages
            },
            "date": chat.date
        }

    def add_message_to_chat(self, db: Session, chat: Chat_Session, user: User, message_type: str, content: str, ai_metadata: Dict = None):
        chat_session = db.query(Chat_Session).filter(
            Chat_Session.id == chat.id,
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).first()

        if not chat_session:
            return {
                "error": "Chat session not found or not active"
            }

        if message_type == "user":
            message_type = Chat_Message_Type.user
        elif message_type == "assistant":
            message_type = Chat_Message_Type.assistant

        new_message = Chat_Message(
            id = get_uuid(Chat_Message, db),
            chat_session_id = chat.id,

            message_type = message_type,
            content = content,
            language = ai_metadata.get("language", "get") if ai_metadata else "en",
            reasoning_data = ai_metadata.get("reasoning_data") if ai_metadata else None,
            knowledge_used = ai_metadata.get("knowledge_used") if ai_metadata else None,
            personalization_appliedv = ai_metadata.get("personalization_applied", False) if ai_metadata else False
        )

        add_db(db, new_message)
        
        chat_session.updated_at = datetime.utcnow()
        update_db(db)

        return {
            "message_id": new_message.id,
            "chat_id": new_message.chat_session_id,
            "type": new_message.message_type,
            "content": new_message.content,
            "date": new_message.date
        }

    def soft_delete_chat_session(self, db: Session, chat: Chat_Session, user: User):
        chat_session = db.query(Chat_Session).filter(
            Chat_Session.id == chat.id,
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).first()

        if not chat_session:
            return {
                "error": "Chat session not found or already deleted"
            }
        
        chat_session.is_active = False,
        chat_session.updated_at = datetime.utcnow()
        update_db(db)

        return {
            "success": True,
            "message": "Chat session deleted successfully",
            "chat_id": chat.id
        }

    def edit_chat_title(self, db: Session, chat: Chat_Session, user: User, new_title: str):
        chat_session = db.query(Chat_Session).filter(
            Chat_Session.id == chat.id,
            Chat_Session.user_id == user.id,
            Chat_Session.is_active == True
        ).first()

        if not chat_session:
            return {
                "error": "Chat session not found or not active"
            }  

        chat_session.title = new_title
        chat_session.updated_at = datetime.utcnow()
        update_db(db)

        return {
            "success": True,
            "message": "Chat title updated successfully",
            "chat_id": chat.id,
            "new_title": new_title
        }

    def get_user_chat_sessions(self, db: Session, user: User, include_inactive: bool = False):
        query = db.query(Chat_Session).filter(
            Chat_Session.user_id == user.id
        )

        if not include_inactive:
            query = query.filter(Chat_Session.is_active == True)

        sessions = query.order_by(Chat_Session.updated_at.desc()).all()

        sessions_data = []

        for session in sessions:
            sessions_data.append({
                "id": session.id,
                "title": session.title,
                "is_active": session.is_active,
                "message_count": len(session.messages),
                "last_message": session.message[-1].content if session.message else None,
                "last_message_time": session.message[-1].date if session.messages else session.date,
                "updated_at": session.updated_at,
                "date": session.date
            })

        return sessions_data
