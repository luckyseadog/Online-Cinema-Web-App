from abc import ABC, abstractmethod


class AbstractCache(ABC):
    @abstractmethod
    async def get_one(self, cache_id: str, entity: object):
        pass

    @abstractmethod
    async def put_one(self, cache_id: str, entity: object) -> None:
        pass

    @abstractmethod
    async def get_many(self, model, cache_id: str) -> list[object]:
        pass

    @abstractmethod
    async def put_many(self, cache_id: str, items: list[object]) -> None:
        pass
