from fastapi import APIRouter, HTTPException
from .services.notifications import notification_service
from .services.orders import orders_service
from app.models import CreateOrderRequest

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/buy")
async def buy(request: CreateOrderRequest):
    order_res = await orders_service.create_order(
        request.user_id,
        request.items,
        request.price,
        request.address
    )

    if order_res.status != "ok":
        raise HTTPException(status_code=400, detail="Order creation failed")

    notification_res = await notification_service.send(
        type="email",
        to="test@test.com",
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
