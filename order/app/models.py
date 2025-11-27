from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    product_id: int
    qty: int


class OrderRequest(BaseModel):
    user_id: int
    items: List[OrderItem]
    address: str
    price: float


class PaymentResponse(BaseModel):
    status: str
    message: str
    order_id: int
    amount: float
    transaction_id: str


class ShippingResponse(BaseModel):
    status: str
    message: str
    order_id: int
    address: str
    tracking_id: str
