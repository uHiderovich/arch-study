from fastapi import APIRouter
from environs import Env

from .notifications import notification_service

env = Env()
env.read_env()

EMAIL_TEST = env("EMAIL_TEST")

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/buy")
def buy():
    notification_service.send(
        type="email",
        to=EMAIL_TEST,
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
