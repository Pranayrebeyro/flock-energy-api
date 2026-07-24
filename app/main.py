from fastapi import FastAPI, HTTPException

from app.client.urja_client import UrjaClient

app = FastAPI(
    title="Flock Energy API"
)


@app.get("/")
async def root():
    return {
        "message": "Flock Energy API is running"
    }


@app.get("/api/v1/meters")
async def meters():

    client = UrjaClient()

    try:
        return await client.get_meters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@app.get("/api/v1/meters/{meter_id}/geo")
async def meter_geo(meter_id: str):

    client = UrjaClient()

    try:
        return await client.get_meter_geo(meter_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@app.get("/api/v1/meters/{meter_id}/energy")
async def meter_energy(meter_id: str):

    client = UrjaClient()

    try:
        return await client.get_meter_energy(meter_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@app.get("/api/v1/meters/{meter_id}")
async def meter(meter_id: str):

    client = UrjaClient()

    try:
        return await client.get_meter(meter_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()