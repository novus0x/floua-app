########## Modules ##########
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Node

from core.utils.generator import get_uuid

# from service.nodes import *

########## Broadcast to all nodes ##########
async def broadcast_all_nodes(msg, nodes):
    for node_id, ws in nodes.items():
        try:
            await ws.send_text(msg)
        except Exception:
            print("[!] Error sending")

########## Broadcast to node (video) ##########
async def broadcast_node_video(msg: str, nodes: dict):
    for node_id, ws in nodes.items():
        try:
            await ws.send_text(msg)
        except Exception:
            print("[!] Error sending")

