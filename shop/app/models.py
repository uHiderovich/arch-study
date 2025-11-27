from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class Product(BaseModel):
    id: int
    name: str
    price: float


class OrderResponse(BaseModel):
    order_id: int
    payment_transaction: str
    shipping_tracking: str
    status: str


class NotificationResponse(BaseModel):
    status: str
    message: str
