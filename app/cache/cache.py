from redis.asyncio import Redis

from app.cache.redis_client import client

class RedisCache:
    def __init__(self, redis: Redis):
        self.redis = redis

        self.__short_code_prefix = "short_code:"
        self.__clicks_prefix = "clicks:"

    async def get_url(self, short_code: str) -> str | None:
        result = await self.redis.get(f"{self.__short_code_prefix}{short_code}")
        await self.redis.incr(f"{self.__clicks_prefix}{short_code}")
        return result

    async def set_url(self, short_code: str, target_url: str) -> bool:
        result = await self.redis.set(f"{self.__short_code_prefix}{short_code}", target_url)
        await self.redis.incr(f"{self.__clicks_prefix}{short_code}")
        return result

    async def delete_url(self, short_code: str) -> None:
        await self.redis.delete(f"{self.__short_code_prefix}{short_code}")
        await self.redis.delete(f"{self.__clicks_prefix}{short_code}")



    async def get_click_by_short_code(self, short_code: list[str]) -> list:
        async with self.redis.pipeline(transaction=True) as pipe:
            for code in short_code:
                await pipe.get(f"{self.__clicks_prefix}{code.split(":")[1]}")
                await pipe.delete(f"{self.__clicks_prefix}{code.split(":")[1]}")


            results = await pipe.execute()
        return results


    async def get_clicks_by_cursor(self, cursor: int = 0, count: int = 50) -> tuple[int, list[dict[str, int]]]:

        cursor, short_code = await self.redis.scan(cursor=cursor, match=f"{self.__clicks_prefix}*", count=count)

        clicks = await self.get_click_by_short_code(short_code)

        clicks_count = []
        for i in range(len(short_code)):

            code = short_code[i].split(":")[1]
            click = int(clicks[i])

            click_data = {
                code: click
            }
            clicks_count.append(click_data)


        # (0, [{'MZKlhF9yXYJW': 2}, ...])
        return cursor, clicks_count

Redis_Cache = RedisCache(client)

