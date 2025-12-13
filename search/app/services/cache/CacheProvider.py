from abc import ABC, abstractmethod

from app.schemas import CacheResponse


class CacheProvider(ABC):
    @abstractmethod
    def get(self, query: str) -> CacheResponse:
        pass

    @abstractmethod
    def set(self, query: str, data: dict):
        pass
