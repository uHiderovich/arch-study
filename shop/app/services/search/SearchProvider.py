from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SearchProvider(ABC):
    @abstractmethod
    async def search(self, product_id: int) -> List[Dict[str, Any]]:
        pass
