########## Modules ##########
from user_agents import parse

from fastapi import APIRouter, Depends, Request

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import User, Chat_Session, Chat_Message_Type

from core.config import settings

from core.utils.http_requests import post_data
from core.utils.responses import custom_response
from core.utils.db_management import add_db, update_db
from core.utils.generator import get_uuid, get_short_id
from core.utils.encrypt import hash_password, check_password, generate_jwt
from core.utils.validators import read_json_body, read_params, validate_required_fields, validate_user

from services.ai.main import Autonomous_Agent

########## Variables ##########
router = APIRouter()
ai_agent = Autonomous_Agent()

########## New Chat ##########
@router.post("/chat/create")
async def create_chat_session(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    new_message, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(new_message, ["title"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    ###  ###
    user_from_db = db.query(User).filter(User.id == user["id"]).first()

    result = ai_agent.create_chat_session(
        db = db,
        user = user_from_db,
        title = new_message.title
    )

    return custom_response(status_code=200, message="Chat created", data={
        "chat": result
    })

########## Chat History ##########
@router.post("/chat/{chat_id}")
async def get_chat_session(request: Request, chat_id: str, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    chat_info, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(chat_info, ["start", "end"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    try:
        start = int(chat_info.start)
        end = int(chat_info.end)
    except:
        return custom_response(status_code=400, message="start/end must be an integer")

    ### Get Chat Session ###
    user_from_db = db.query(User).filter(User.id == user["id"]).first()
    chat = db.query(Chat_Session).filter(Chat_Session.id == chat_id).first()

    if not chat:
        return custom_response(status_code=400, message="The chat does not exist")

    messages_result = ai_agent.get_chat_messages(
        db = db,
        chat = chat,
        user = user_from_db,
        start = start,
        finish = end
    )

    if "error" in messages_result:
        return custom_response(status_code=400, message="Something went wrong...")

    return custom_response(status_code=200, message="Chat History", data={
        "chat": messages_result
    })

########## New Message ##########
@router.post("/chat/new-message")
async def send_new_message(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Body ###
    new_message, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(new_message, ["chat_id", "message"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    ### Get Chat Session ###
    user_from_db = db.query(User).filter(User.id == user["id"]).first()
    chat = db.query(Chat_Session).filter(Chat_Session.id == chat_id).first()

    if not chat:
        return custom_response(status_code=400, message="The chat does not exist")

    user_message_result = ai_agent.add_chat_message(
        db = db,
        chat = chat,
        user = user_from_db,
        message_type = Chat_Message_Type.user,
        content = new_message["message"]
    )

    ai_response = ai_agent.process_interaction(
        db = db,
        user_input = new_message["message"],
        user = user_from_db
    )

    ai_message_result = ai_agent.add_chat_message(
        db = db,
        chat = chat,
        user = user_from_db,
        message_type = Chat_Message_Type.assistant,
        content = ai_response["response"],
        ai_metadata = {
            "language": ai_response["language"],
            "reasoning_process": ai_response.get("reasoning_process"),
            "knowledge_used": ai_response.get("used_official_knowledge"),
            "personalization_applied": ai_response.get("personalization_applied", False)
        }
    )
    
    return custom_response(status_code=200, message="Ok", data={
        "user_message": user_message_result,
        "ai_response": {
            "message_id": ai_message_result["message_id"],
            "content": ai_response["response"],
            "metadata": {
                "language": ai_response["language"],
                "used_official_knowledge": ai_response.get("used_official_knowledge", Falses),
                "personalization_applied": ai_response.get("personalization_applied", False)
            }
        }
    })

########## Get Sessions ##########
@router.get("/chat/sessions/active")
async def list_active_chat_sessions(request: Request, db: Session = Depends(get_db)):
    ### Get Session ###
    user, error = await validate_user(request, db, True)
    if error:
        return custom_response(status_code=400, message=error)

    ### Get Chat Session ###
    user_from_db = db.query(User).filter(User.id == user["id"]).first()

    ###  ###
    sessions = ai_agent.get_active_chat_sessions(db, user_from_db)
    
    return custom_response(status_code=200, message="Active Chats", data={
        "sessions": sessions,
        "total_sessions": len(sessions)
    })
