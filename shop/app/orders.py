from fastapi import APIRouter

from .services.notifications import notification_service
from .services.orders import orders_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/buy")
def buy():
    notification_service.send(
        type="email",
        to="test@test.com",
        title="Ваш заказ принят",
        message="Спасибо за покупку!"
    )
    return "Order created!"


@router.post("/subscribe")
def subscribe(subscription: dict):
    notification_service.send(
        type="push",
        subscription=subscription,
        title="Подписка на уведомления",
        message="Спасибо за подписку!"
    )
    return "Subscription created!"


@router.post("/checkout")
async def checkout(order_id: int, amount: float, address: str):
    order_res = await orders_service.create_order(
        order_id,
        amount,
        address
    )
    return order_res
