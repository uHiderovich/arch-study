from environs import Env
from .HttpShippingProvider import HttpShippingProvider

env = Env()
env.read_env()

shipping_service = HttpShippingProvider(
    url=env("SHIPPING_SERVICE_URL"),
)
