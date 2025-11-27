from environs import Env
from .HttpOrderProvider import HttpOrderProvider

env = Env()
env.read_env()

orders_service = HttpOrderProvider(
    url=env("ORDERS_SERVICE_URL"),
)
