import httpx

from .OrderProvider import OrderProvider
from app.models import OrderResponse
from typing import List
from app.models import OrderItem


status_map = {
    "completed": "ok",
    "failed": "error"
}


class HttpOrderProvider(OrderProvider):
    def __init__(self, url: str):
        self.url = url

    async def create_order(
        self,
        user_id: int,
        items: List[OrderItem],
        price: float,
        address: str
    ) -> OrderResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.url}/process/order", json={
                "user_id": user_id,
                "items": [item.model_dump() for item in items],
                "price": price,
                "address": address
            })
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status")
            data["status"] = status_map.get(status, status)
            return OrderResponse(**data)
