import httpx
from typing import Any
from .CacheProvider import CacheProvider
from app.schemas import CacheResponse
from app.schemas import Product


class HttpCacheProvider(CacheProvider):
    def __init__(self, url: str):
        self.url = url

    async def get(self, query: str) -> CacheResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.url}/get-cache",
                params={"query": query}
            )
            resp.raise_for_status()
            data = resp.json().get("data")
            return CacheResponse(data=[Product(**r) for r in data] if data else None)

    async def set(self, query: str, data: Any):
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.url}/save-cache",
                json={"query": query, "data": data}
            )
