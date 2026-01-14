from fastapi import APIRouter, HTTPException

from app.services.notifications import notification_service
from app.services.orders import orders_service
from app.models import CreateOrderRequest
from monitoring.counters import ORDERS_CREATED, ORDERS_FAILED


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
        ORDERS_FAILED.inc()
        raise HTTPException(status_code=400, detail="Order creation failed")

    ORDERS_CREATED.inc()

    try:
        notification_service.send_create_order_email(
            to="test@test.com",
            title="Ваш заказ принят",
            message="Спасибо за покупку!"
        )
    except Exception as e:
        print("Notification sending failed", e)

    return order_res


@router.post("/subscribe")
async def subscribe(subscription: dict):
    await notification_service.send(
        type="push",
        subscription=subscription,
        title="Подписка на уведомления",
        message="Спасибо за подписку!"
    )
