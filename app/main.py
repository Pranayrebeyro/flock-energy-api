from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

from app.config import settings
from app.client.urja_client import UrjaClient


app = FastAPI(
    title="Flock Energy API",
    version="0.1.0",
    debug=True
)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    print("\n========== ERROR ==========")

    traceback.print_exc()

    print("===========================\n")


    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc)
        }
    )


@app.get("/")
async def root():

    return {
        "message": "Flock Energy API is running"
    }


@app.get("/api/v1/meters/{meter_id}")
async def get_meter(
    meter_id: str
):

    client = UrjaClient()

    try:

        result = await client.get_meter(
            meter_id
        )

        return result

    finally:

        await client.close()