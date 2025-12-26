import pika

from abc import ABC, abstractmethod
from typing import Dict, Callable
from environs import Env

env = Env()
env.read_env()


class Connection(ABC):
    @abstractmethod
    def declare_queue(self, event_type: str, callback: Callable, queue_name: str | None = None):
        pass

    @abstractmethod
    def start_consuming(self):
        pass

    @abstractmethod
    def close(self):
        pass


class RabbitConnection(Connection):
    def __init__(self, exchange: str, routing_keys: Dict[str, str]):
        self._exchange = exchange
        self._routing_keys = routing_keys

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

        self._connection = pika.BlockingConnection(self._params)
        self._channel = self._connection.channel()

        # гарантируем существование exchange
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type="direct",
            durable=True
        )

    def declare_queue(self, event_type: str, callback: Callable, queue_name: str | None = None):
        if queue_name is None:
            queue_name = f"email_queue_{event_type}"

        declare_ok = self._channel.queue_declare(queue=queue_name, durable=True)
        print(f"Queue {declare_ok.method.queue}")

        self._channel.queue_bind(
            exchange=self._exchange,
            queue=declare_ok.method.queue,
            routing_key=self.get_routing_key(event_type)
        )

        self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            queue=declare_ok.method.queue,
            on_message_callback=callback
        )
        print("Declare ended")

    def get_routing_key(self, event_type: str) -> str:
        return self._routing_keys[event_type]

    def start_consuming(self):
        print("Start consuming")
        self._channel.start_consuming()

    def close(self):
        if self._connection and not self._connection.is_closed:
            self._connection.close()
