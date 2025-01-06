from redis.asyncio import Redis


def redis_connection(settings) -> Redis:
    return Redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )
