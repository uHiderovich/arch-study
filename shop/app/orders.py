from fastapi import APIRouter, HTTPException

from .services.notifications import notification_service
from .services.orders import orders_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/buy")
async def buy(order_id: int, amount: float, address: str):
    order_res = await orders_service.create_order(
        order_id,
        amount,
        address
    )

    if order_res.status != "ok":
        raise HTTPException(status_code=400, detail="Order creation failed")

    notification_res = await notification_service.send(
        type="email",
        to=order_res.email,
        title="Ваш заказ принят",
        message="Спасибо за покупку!"
    )

    if notification_res.status != "ok":
        raise HTTPException(status_code=400, detail="Notification sending failed")

    return order_res


@router.post("/subscribe")
async def subscribe(subscription: dict):
    await notification_service.send(
        type="push",
        subscription=subscription,
        title="Подписка на уведомления",
        message="Спасибо за подписку!"
    )
