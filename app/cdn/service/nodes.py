########## Modules ##########
from sqlalchemy.orm import Session

from db.database import get_db
from db.model import Node

from core.utils.generator import get_uuid
from core.utils.ws import broadcast_all_nodes

########## Select best node ##########
async def best_node_upload(nodes, db: Session):
    # nodes = db.query(Node).filter(Node.active)
    return "ok"
