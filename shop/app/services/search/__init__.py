from environs import Env
from .HttpSearchProvider import HttpSearchProvider

env = Env()
env.read_env()

search_service = HttpSearchProvider(
    url=env("SEARCH_SERVICE_URL"),
)
