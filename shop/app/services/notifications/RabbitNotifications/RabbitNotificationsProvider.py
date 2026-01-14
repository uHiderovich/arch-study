from typing import Dict
from ..NotificationProvider import NotificationProvider
from .Connection import Connection
from dataclasses import dataclass, asdict
from monitoring.counters import EVENTS_PUBLISHED, EVENT_PUBLISH_ERRORS


@dataclass
class EmailEvent:
    to: str
    title: str
    message: str


class PikaNotificationProvider(NotificationProvider):
    def __init__(self, connection: Connection):
        self._connection = connection

    def send(self, event_type: str, body: Dict[str, any]):
        try:
            self._connection.publish(event_type, body)
            EVENTS_PUBLISHED.labels(event_type=event_type).inc()
        except Exception as e:
            EVENT_PUBLISH_ERRORS.inc()
            print(f"Failed to publish event {event_type}: {e}")
            raise

    def send_create_order_email(self, to: str, title: str, message: str):
        self.send("OrderCreated", asdict(EmailEvent(to, title, message)))
