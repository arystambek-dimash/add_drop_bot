from redis import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value, expire=3600):
        return await self.redis.set(key, value, ex=expire)

    async def delete(self, key):
        return await self.redis.delete(key)
