import json
import pika

from abc import ABC, abstractmethod
from typing import Dict, Any


class Connection(ABC):
    @abstractmethod
    def publish(self, event_type: str, body: Dict[str, Any]):
        pass

    @abstractmethod
    async def close(self):
        pass


class RabbitConnection(Connection):
    def __init__(self, host: str):
        self._exchange = "shop.events"
        self._routing_keys = {
            "OrderCreated": "order.created"
        }

        params = pika.ConnectionParameters(
            host=host,
            heartbeat=30,
            blocked_connection_timeout=300
        )

        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()

        # гарантируем существование exchange
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type="direct",
            durable=True
        )

        # включаем confirm
        self._channel.confirm_delivery()

    def get_routing_key(self, event_type: str) -> str:
        return self._routing_keys[event_type],

    def publish(self, event_type: str, body: Dict[str, Any]):
        routing_key = self.get_routing_key(event_type)
        if routing_key:
            self._channel.basic_publish(
                exchange=self._exchange,
                routing_key=routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )
        else:
            raise ValueError(f"Invalid event type: {event_type}")

    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
