from abc import ABC, abstractmethod

from app.models import NotificationResponse


class NotificationProvider(ABC):
    @abstractmethod
    def send(self, type: str, **kwargs) -> NotificationResponse:
        pass
