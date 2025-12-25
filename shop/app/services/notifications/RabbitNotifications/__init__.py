from environs import Env

from .Connection import RabbitConnection
from .RabbitNotificationsProvider import RabbitNotificationsProvider

env = Env()
env.read_env()

connection = RabbitConnection(host=env("RABBIT_HOST"))

rabbit_provider = RabbitNotificationsProvider(connection)
