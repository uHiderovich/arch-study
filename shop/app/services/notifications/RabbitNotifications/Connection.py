import json
import pika
import time

from abc import ABC, abstractmethod
from typing import Dict, Any

from environs import Env

env = Env()
env.read_env()


class Connection(ABC):
    @abstractmethod
    def publish(self, event_type: str, body: Dict[str, Any]):
        pass

    @abstractmethod
    def close(self):
        pass


class RabbitConnection(Connection):
    def __init__(self):
        self._exchange = "shop.events"
        self._routing_keys = {
            "OrderCreated": "order.created"
        }

        credentials = pika.PlainCredentials(
            username=env("RABBITMQ_DEFAULT_USER"),
            password=env("RABBITMQ_DEFAULT_PASS")
        )

        self._params = pika.ConnectionParameters(
            host=env("RABBIT_HOST"),
            heartbeat=30,
            blocked_connection_timeout=300,
            credentials=credentials,
        )

        self._connection = None
        self._channel = None
        self._ensure_connection()

    def _ensure_connection(self):
        """Создает или пересоздает соединение с RabbitMQ"""
        try:
            if self._connection is None or self._connection.is_closed:
                self._connection = pika.BlockingConnection(self._params)
                self._channel = self._connection.channel()

                # гарантируем существование exchange
                self._channel.exchange_declare(
                    exchange=self._exchange,
                    exchange_type="direct",
                    durable=True
                )

                # включаем confirm для проверки доставки
                self._channel.confirm_delivery()
        except Exception as e:
            print(f"Failed to establish RabbitMQ connection: {e}")
            raise

    def _reconnect(self):
        """Переподключается к RabbitMQ"""
        try:
            self.close()
            time.sleep(1)  # Небольшая задержка перед переподключением
            self._ensure_connection()
        except Exception as e:
            print(f"Failed to reconnect to RabbitMQ: {e}")
            raise

    def get_routing_key(self, event_type: str) -> str:
        return self._routing_keys[event_type]

    def publish(self, event_type: str, body: Dict[str, Any], max_retries: int = 3):
        """Публикует событие с retry логикой"""
        routing_key = self.get_routing_key(event_type)
        if not routing_key:
            raise ValueError(f"Invalid event type: {event_type}")

        for attempt in range(max_retries):
            try:
                # Проверяем соединение перед публикацией
                if self._connection is None or self._connection.is_closed:
                    self._reconnect()

                # Публикуем с persistent delivery mode
                # При включенном confirm_delivery() исключение будет выброшено автоматически при проблемах
                self._channel.basic_publish(
                    exchange=self._exchange,
                    routing_key=routing_key,
                    body=json.dumps(body),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Persistent delivery
                        content_type="application/json"
                    )
                )

                return  # Успешная публикация (если нет исключения)

            except (pika.exceptions.ConnectionClosed, pika.exceptions.StreamLostError, Exception) as e:
                if attempt < max_retries - 1:
                    print(f"Publish attempt {attempt + 1} failed: {e}. Retrying...")
                    self._reconnect()
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                else:
                    print(f"Failed to publish after {max_retries} attempts: {e}")
                    raise

    def close(self):
        if self._connection and not self._connection.is_closed:
            try:
                self._connection.close()
            except Exception:
                pass
