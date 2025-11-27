from environs import Env
from .HttpNotificationProvider import HttpNotificationProvider

env = Env()
env.read_env()

notification_service = HttpNotificationProvider(
    email_url=env("EMAIL_SERVICE_URL"),
    push_url=env("PUSH_SERVICE_URL"),
)
