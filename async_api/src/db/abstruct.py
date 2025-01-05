from abc import ABC, abstractmethod


class CacheInterface(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        pass

    @abstractmethod
    async def set(self, **kwargs):
        pass

class StorageInterface(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        pass

    @abstractmethod
    async def search(self, **kwargs):
        pass
