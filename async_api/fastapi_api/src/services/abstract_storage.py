from abc import ABC, abstractmethod

class AbstractStorage(ABC):
    @abstractmethod
    async def get_all(self, **kwargs):
        pass

    @abstractmethod
    async def search(self, **kwargs):
        pass

    @abstractmethod
    async def get_by_id(self, **kwargs):
        pass
