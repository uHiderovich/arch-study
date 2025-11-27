import httpx

from .PaymentProvider import PaymentProvider
from app.models import PaymentResponse


class HttpPaymentProvider(PaymentProvider):
    def __init__(self, url: str):
        self.url = url

    async def create_payment(self, order_id: int, amount: float) -> PaymentResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.url}/process/pay", json={
                "order_id": order_id,
                "amount": amount,
            })
            resp.raise_for_status()
            return PaymentResponse(**resp.json())
