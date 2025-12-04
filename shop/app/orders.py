from fastapi import APIRouter, HTTPException, Query
from .services.notifications import notification_service
from .services.orders import orders_service
from app.models import CreateOrderRequest
import httpx
from environs import Env

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

env = Env()
env.read_env()

SEARCH_URL = env("SEARCH_SERVICE_URL")


@router.get("/search")
async def shop_search(q: str = Query(...), category: int | None = Query(None)):
    params = {"q": q}
    if category is not None:
        params["category"] = category
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SEARCH_URL}/search", params=params)
        r.raise_for_status()
        return r.json()
