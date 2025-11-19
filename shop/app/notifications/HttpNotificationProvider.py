import requests
from .NotificationProvider import NotificationProvider


class HttpNotificationProvider(NotificationProvider):
    def __init__(self, email_url: str, push_url: str):
        self.email_url = email_url
        self.push_url = push_url

    def send(self, type: str, **kwargs):
        to = kwargs.get("to", None)
        subscription = kwargs.get("subscription", None)
        title = kwargs.get("title", None)
        message = kwargs.get("message", None)

        if type == "email":
            self.send_email(to, title, message)
        elif type == "push":
            self.send_push(subscription, title, message)
        else:
            raise ValueError(f"Invalid notification type: {type}")

    def send_email(self, to, subject, message):
        requests.post(
            f"{self.email_url}/send-email",
            json={"to": to, "subject": subject, "message": message}
        )

    def send_push(self, subscription, title, body):
        requests.post(
            f"{self.push_url}/send-push",
            json={"subscription": subscription, "title": title, "body": body}
        )
