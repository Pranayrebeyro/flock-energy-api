from fastapi import APIRouter, HTTPException

from app.client.urja_client import UrjaClient

router = APIRouter()

client = UrjaClient()


@router.get("/meters")
async def get_meters():
    try:
        data = await client.get_meters()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))