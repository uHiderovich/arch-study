from abc import ABC, abstractmethod


class NotificationProvider(ABC):

    @abstractmethod
    def send_email(self, to: str, subject: str, message: str):
        pass

    @abstractmethod
    def send_push(self, subscription: dict, title: str, body: str):
        pass
