from pydantic import BaseModel


class ShippingRequest(BaseModel):
    order_id: int
    address: str
