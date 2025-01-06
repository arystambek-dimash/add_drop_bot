from typing import Protocol


class IRedisRepository(Protocol):
    async def get(self, key):
        pass

    async def set(self, key, value, expire=3600):
        pass

    async def delete(self, key):
        pass
