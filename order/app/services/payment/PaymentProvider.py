from abc import ABC, abstractmethod

from app.models import PaymentResponse


class PaymentProvider(ABC):
    @abstractmethod
    async def create_payment(self, order_id: int, amount: float) -> PaymentResponse:
        pass
