from pydantic import BaseModel


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
