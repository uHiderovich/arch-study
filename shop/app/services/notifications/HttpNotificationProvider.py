import httpx

from .NotificationProvider import NotificationProvider
from app.models import NotificationResponse


class HttpNotificationProvider(NotificationProvider):
    def __init__(self, email_url: str, push_url: str):
        self.email_url = email_url
        self.push_url = push_url

    async def send(self, type: str, **kwargs) -> NotificationResponse:
        to = kwargs.get("to", None)
        subscription = kwargs.get("subscription", None)
        title = kwargs.get("title", None)
        message = kwargs.get("message", None)

        if type == "email":
            return await self.send_email(to, title, message)
        elif type == "push":
            return await self.send_push(subscription, title, message)
        else:
            raise ValueError(f"Invalid notification type: {type}")

    async def send_email(self, to, subject, message):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.email_url}/send-email",
                json={"to": to, "subject": subject, "message": message}
            )
            resp.raise_for_status()
            return NotificationResponse(**resp.json())

    async def send_push(self, subscription, title, body):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.push_url}/send-push",
                json={
                    "subscription": subscription,
                    "title": title,
                    "body": body
                }
            )
            resp.raise_for_status()
            return NotificationResponse(**resp.json(), message="Push sent!")
