import httpx

from .OrderProvider import OrderProvider
from app.models import OrderResponse


class HttpOrderProvider(OrderProvider):
    def __init__(self, url: str):
        self.url = url

    async def create_order(self, order_id: int, amount: float, address: str) -> OrderResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.url}/process/order", json={
                "order_id": order_id,
                "amount": amount,
                "address": address
            })
            resp.raise_for_status()
            return OrderResponse(**resp.json())
