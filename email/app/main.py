import json

from .connection import RabbitConnection
from .email_sender import send_email


exchange = "shop.events"
routing_keys = {
    "OrderCreated": "order.created"
}

connection = RabbitConnection(
    exchange=exchange,
    routing_keys=routing_keys
)


def callback(ch, method, properties, body: str):
    print(f"Received message: {body}")
    event = json.loads(body)
    send_email(event["to"], event["title"], event["message"])
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    print("Email service started")
    try:
        connection.declare_queue("OrderCreated", callback)
        connection.start_consuming()

    except KeyboardInterrupt:
        print("Stopping worker…")

    finally:
        # гарантированно закроем соединение
        connection.close()
        print("RabbitMQ connection closed")


if __name__ == "__main__":
    print("Start service")
    main()
