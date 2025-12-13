from environs import Env
from .HttpCacheProvider import HttpCacheProvider

env = Env()
env.read_env()

cache_service = HttpCacheProvider(
    url=env("CACHE_SERVICE_URL"),
)
