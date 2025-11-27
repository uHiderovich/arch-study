from environs import Env
from .HttpPaymentProvider import HttpPaymentProvider

env = Env()
env.read_env()

payment_service = HttpPaymentProvider(
    url=env("PAYMENT_SERVICE_URL"),
)
