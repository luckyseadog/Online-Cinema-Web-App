from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    async def get_all(self, *args, **kwargs) -> list:
        pass

    @abstractmethod
    async def search(self, *args, **kwargs) -> list:
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> object:
        pass
