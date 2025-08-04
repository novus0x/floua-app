########## Modules ##########
import os, json, websockets, datetime

from pathlib import Path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request, status, UploadFile, File

from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Allowed_Node, Node, Video, Upload_Token

from core.utils.responses import custom_response
from core.utils.generator import get_uuid
from core.utils.validators import read_json_body, validate_required_fields
from core.utils.ws import broadcast_node_video

########## Variables ##########
router = APIRouter()
router_ws = APIRouter()

allowed_exts = [".mp4", ".mov", ".mkv"]

WS_URL = "ws://192.168.1.36:3003"

########## Websocket nodes ##########
connected_nodes = {}

########## Accept connections ##########
@router_ws.websocket("/connect")
async def home(websocket: WebSocket, db: Session = Depends(get_db)):
    ### Check if valid node ###
    ip, _ = websocket.client

    node = db.query(Allowed_Node).filter(Allowed_Node.ip == ip).first()
    if not node:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print("[!] Unauthorize connection: " + ip)
        return False

    if node.active == False:
        print("[!] Unauthorize connection " + node.ip)
        return False
    
    ### Accept connection ###
    await websocket.accept()
    node_id = await get_uuid(Node, db)
    connected_nodes[node_id] = websocket

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data["type"] == "register":
                node = db.query(Node).filter(Node.ip == ip).first()

                if not node: ### New connection
                    new_node = Node(
                        id = node_id,
                        ip = data["node_info"]["ip"],
                        port = data["node_info"]["port"],
                    )
                    db.add(new_node)
                    db.commit()
                    db.refresh(new_node)
                else: ### Reconnecting
                    node.last_seen = datetime.datetime.utcnow()
                    node.active = True
                    db.commit()
                
    except WebSocketDisconnect:
        node = db.query(Node).filter(Node.ip == ip).first()
        if node:
            node.active = False
            db.commit()

        connected_nodes.pop(node_id, None)


########## Add Node ##########
@router.post("/add")
async def add(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    node, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)
    
    ### Validations ###
    required_fields, error = validate_required_fields(node, ["node_ip"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)

    if db.query(Allowed_Node).filter(Allowed_Node.ip == node.node_ip).first():
        return custom_response(status_code=400, message="Node already added")

    ### Save to DB ###
    new_allowed_node = Allowed_Node(
        id = await get_uuid(Allowed_Node, db),
        ip = node.node_ip,
    )

    db.add(new_allowed_node)
    db.commit()
    db.refresh(new_allowed_node)

    return custom_response(status_code=201, message="Node added")

########## Get node answer ##########
@router.post("/video_status")
async def video_status(request: Request, db: Session = Depends(get_db)):
    ### Get Body ###
    video, error = await read_json_body(request)
    if error: 
        return custom_response(status_code=400, message=error)

    ### Validations ###
    required_fields, error = validate_required_fields(video, ["video_id", "status"])
    if error:
        return custom_response(status_code=400, message="Fields required", details=required_fields)
    
    print(video)

    return "ok"
