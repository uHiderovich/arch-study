from abc import ABC, abstractmethod

from app.models import OrderResponse


class OrderProvider(ABC):
    @abstractmethod
    async def create_order(self, order_id: int, amount: float, address: str) -> OrderResponse:
        pass
