########## Modules ##########
import httpx

from core.config import settings

########## POST Data ##########
async def post_data_api(endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(settings.BACKEND_ORIGIN + endpoint, json=data)
        return res.json()

########## POST Data to Media Service ##########
async def post_data(endpoint: str, fileobj, data: dict):
    files = { "file": (data["filename"], fileobj, "application/octet-stream") }

    async with httpx.AsyncClient() as client:
        res = await client.post(settings.MEDIA_ORIGIN + endpoint, files=files, data=data)

        # print(res.json())

########## POST Data to Media Service - Download ##########
async def post_download_file(endpoint: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(settings.MEDIA_ORIGIN + endpoint, json=data)

            if res.status_code == 200:
                with open(data["location"], "wb") as f:
                    f.write(res.content)
            else:
                print("Error")
            
            print(res.json())
    except Exception as e:
        print(e)

########## POST Data to Media Service - Signed url ##########
async def post_signed_url(endpoint: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(settings.MEDIA_ORIGIN + endpoint, json=data)
            
            # print(res.json())
    except Exception as e:
        print(e)