from typing import Dict
from ..NotificationProvider import NotificationProvider
from .Connection import Connection
from dataclasses import dataclass, asdict


@dataclass
class EmailEvent:
    to: str
    title: str
    message: str


class PikaNotificationProvider(NotificationProvider):
    def __init__(self, connection: Connection):
        self._connection = connection

    def send(self, event_type: str, body: Dict[str, any]):
        self._connection.publish(event_type, body)

    def send_create_order_email(self, to: str, title: str, message: str):
        self.send("OrderCreated", asdict(EmailEvent(to, title, message)))
