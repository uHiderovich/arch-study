import httpx

from .SearchProvider import SearchProvider
from typing import List, Dict, Any


class HttpSearchProvider(SearchProvider):
    def __init__(self, url: str):
        self.url = url

    async def search(self, product_id: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/search",
                params={"product_id": product_id}
            )
            response.raise_for_status()
            return response.json()
