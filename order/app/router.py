from fastapi import APIRouter, HTTPException
from .models import OrderRequest
from .services.payment import payment_service
from .services.shipping import shipping_service

router = APIRouter(prefix="/process", tags=["order-processing"])


@router.post("/order")
async def create_order(order: OrderRequest):
    """
    Контроллер создаёт заказ, вызывает Payment → Shipping.
    В реальном проекте заказ бы сохранялся в БД.
    """

    # Простейший идентификатор заказа
    order_id = 12345

    # 1. Платёж
    payment = await payment_service.create_payment(order_id, order.price)

    if payment.status != "ok":
        raise HTTPException(status_code=400, detail="Payment failed")

    # 2. Доставка
    shipping = await shipping_service.ship_order(order_id, order.address)

    if shipping.status != "ok":
        raise HTTPException(status_code=400, detail="Shipping failed")

    # 3. Итоговый ответ клиенту
    return {
        "order_id": order_id,
        "payment_transaction": payment.transaction_id,
        "shipping_tracking": shipping.tracking_id,
        "status": "completed"
    }
