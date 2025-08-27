########## Modules ##########
import httpx

from fastapi import UploadFile

from core.config import settings

########## POST Data ##########
async def post_data(endpoint: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(settings.NODE_ORIGIN + endpoint, json=data)
    except Exception as e:
        print(e)

########## POST Data ##########
async def post_data_api(endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(settings.BACKEND_ORIGIN + endpoint, json=data)
        return res.json()

########## POST Data to Media Service ##########
async def post_data_media(endpoint: str, file: UploadFile, data: dict):
    async with httpx.AsyncClient() as client:
        files_bytes = await file.read()
        files = { "file": (file.filename, files_bytes) }
        res = await client.post(settings.MEDIA_ORIGIN + endpoint, files=files, data=data)

        print(res.json())

########## POST - Signed url ##########
async def post_signed_url(endpoint: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(settings.MEDIA_ORIGIN + endpoint, json=data)
            data = res.json()

            return data["url"]
    except Exception as e:
        print(e)
