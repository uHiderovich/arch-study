import httpx

from .ShippingProvider import ShippingProvider
from app.models import ShippingResponse


class HttpShippingProvider(ShippingProvider):
    def __init__(self, url: str):
        self.url = url

    async def ship_order(self, order_id: int, address: str) -> ShippingResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.url}/process/ship", json={
                "order_id": order_id,
                "address": address
            })
            resp.raise_for_status()
            return ShippingResponse(**resp.json())
