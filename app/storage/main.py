########## Modules ##########
import os, asyncio, json, websockets, base64, uuid, shutil

from pathlib import Path

from core.config import settings
from db.database import Base, engine, get_db

from db.model import Video

from core.utils.generator import get_uuid
from core.utils.net import get_local_ip

########## Create tables ##########
Base.metadata.create_all(bind=engine)

########## Variables ##########
connected_nodes = {}
base_url = "ws://" + settings.CDN_ORIGIN
ORIGIN = "192.168.1.36"
SAVE_DIR = Path("videos").absolute()

### Check folder ###
SAVE_DIR.mkdir(parents=True, exist_ok=True)

########## Create server ##########
async def handle_upload(websocket):
    ### Access DB ###
    db_gen = get_db()
    try:
        db = next(db_gen)  
    except:
        db_gen.close()

    file = None
    file_dir = None

    try:
        async for message in websocket:
            if isinstance(message, str):

                data = json.loads(message)

                if data["type"] == "upload_init": ### Start downloading the file
                    filename = data["video_info"]["filename"]
                    file_uuid = data["video_info"]["video_id"]
                    ext = Path(filename).suffix
                    
                    file_dir = SAVE_DIR / file_uuid
                    file_dir.mkdir(parents=True, exist_ok=True) 

                    file_path = file_dir / f"{file_uuid}{ext}"
                    file = open(file_path, "wb")
                elif data["type"] == "upload_end": ### Downloaded file
                    break
            
            elif isinstance(message, bytes) and file:
                file.write(message)

        if file: ### Success
            new_video = Video(id = file_uuid)
            db.add(new_video)
            db.commit()
            db.flush(new_video)
            file.close()

    except Exception as e: ### Error
        if file:
            file.close()

        if file_dir and file_dir.exists():
            shutil.rmtree(file_dir)

########## Connect to server ##########
async def handle_connection():
    async with websockets.connect(base_url + "/ws/connect") as websocket:
        ip = get_local_ip()

        if ip == "127.0.0.1":
            return "DDD"

        register_msg = {
            "type": "register",
            "node_info": {
                "ip": ip,
                "port": settings.PORT
            }
        }

        await websocket.send(json.dumps(register_msg))

        while True:
            msg = await websocket.recv()
            print(msg)
    
########## Main function ##########
async def main():
    ### Client ###
    client = asyncio.create_task(handle_connection())

    ### Server ###
    server = await websockets.serve(handle_upload, "0.0.0.0", settings.PORT)
    await asyncio.gather(client)

########## Init ##########
asyncio.run(main())
