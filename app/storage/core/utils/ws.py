########## Modules ##########
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Node

from core.utils.generator import get_uuid

########## Broadcast to all nodes ##########
async def broadcast_all(msg: str, nodes: dict):
    for node_id, ws in nodes.items():
        try:
            await ws.send_text(msg)
        except Exception:
            print("[!] Error sending")
