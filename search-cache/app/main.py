from fastapi import FastAPI, Query, Body
from app.models import CacheResponse
from app.storage import cache_storage
from app.models import Product

app = FastAPI(title="Search Cache Service")


@app.get("/get-cache")
async def get_cache(query: str = Query(...)):
    try:
        result = await cache_storage.get(query)
        return CacheResponse(data=[Product(**r) for r in list(result)] if result else None)
    except Exception as e:
        print(f"Error getting cache: {e}")
        return CacheResponse(data=None)


@app.post("/save-cache")
async def save_cache(data: dict = Body(...)):
    query = data.get("query")
    data = data.get("data")
    try:
        await cache_storage.set(query, data)
    except Exception as e:
        print(f"Error saving cache: {e}")
