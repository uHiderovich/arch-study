from .RabbitNotifications.Connection import RabbitConnection
from .RabbitNotifications.RabbitNotificationsProvider import PikaNotificationProvider


connection = RabbitConnection()
notification_service = PikaNotificationProvider(connection)
