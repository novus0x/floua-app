########## Modules ##########
import httpx

from core.config import settings

########## GET Data ##########
async def get_data(endpoint: str):
    async with httpx.AsyncClient() as client:
        res = await client.get()
        return res.json()

########## POST Data ##########
async def post_data(endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(settings.CDN_ORIGIN + endpoint, json=data)
        return res.json()
