from redis.asyncio import StrictRedis
from environs import Env
from abc import ABC, abstractmethod
import json
from typing import Any

env = Env()
env.read_env()

redis = StrictRedis(
    host=env("REDIS_HOST"),
    port=env("REDIS_PORT"),
    db=env("REDIS_DATABASE"),
    password=env("REDIS_PASSWORD"),
    username=env("REDIS_USERNAME"),
    decode_responses=True,
)


class Storage(ABC):
    @abstractmethod
    async def set(key: str, data: Any):
        pass

    @abstractmethod
    async def get(key: str):
        pass


class RedisStorage(Storage):
    def __init__(self, redis: StrictRedis):
        self.redis = redis

    async def set(self, key: str, data: Any):
        await redis.set(key, json.dumps(data), ex=env("EXPIRE_TIME"))

    async def get(self, key: str):
        raw = await self.redis.get(key)
        return json.loads(raw) if raw else None


class CacheStorage(Storage):
    def __init__(self, storage: Storage):
        self.storage = storage

    def make_key(self, query: str) -> str:
        return hash(query)

    async def set(self, query: str, data: Any):
        await self.storage.set(self.make_key(query), data)

    async def get(self, query: str):
        return await self.storage.get(self.make_key(query))


cache_storage = CacheStorage(RedisStorage(redis))
