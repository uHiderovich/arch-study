from fastapi import APIRouter
import requests
from environs import Env


env = Env()
env.read_env()

EMAIL_TEST = env("EMAIL_TEST")

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/send-email")
def buy():
    # отправляем письмо через микросервис
    requests.post(
        "http://email-service:5001/send-email",
        json={
            "to": EMAIL_TEST,
            "subject": "Ваш заказ принят",
            "message": "Спасибо за покупку!"
        }
    )
    return "Order created!"


@router.post("/send-push")
def notify_user(subscription, title, body):
    requests.post(
        "http://push-service:5002/send-push",
        json={
            "subscription": subscription,
            "title": title,
            "body": body
        }
    )
