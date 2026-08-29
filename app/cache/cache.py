from redis.asyncio import Redis

from app.cache.redis_client import client

class RedisCache:
    def __init__(self, redis: Redis):
        self.redis = redis

        self.__short_code_prefix = "short_code:"

    async def get_url(self, short_code: str) -> str | None:

        result = await self.redis.get(f"{self.__short_code_prefix}{short_code}")
        return result

    async def set_url(self, short_code: str, target_url: str) -> bool:
        result = await self.redis.set(f"{self.__short_code_prefix}{short_code}", target_url)
        return result

    async def delete_url(self, short_code: str) -> None:
        await self.redis.delete(f"{self.__short_code_prefix}{short_code}")


Redis_Cache = RedisCache(client)
