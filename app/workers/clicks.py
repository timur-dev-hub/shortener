import asyncio

from app.cache.cache import Redis_Cache

async def clicks_synchronization():
    while True:


        cursor, clicks_count = await Redis_Cache.get_clicks_by_cursor()

        while cursor != 0:

            data = await Redis_Cache.get_clicks_by_cursor(cursor=cursor)
            clicks_count += data[1]
            cursor = data[0]

        clicks = {}

        for i in clicks_count:
            clicks.update(i)


        await asyncio.sleep(600)



