from abc import ABC, abstractmethod

from app.models import ShippingResponse


class ShippingProvider(ABC):
    @abstractmethod
    async def ship_order(self, order_id: int, address: str) -> ShippingResponse:
        pass
