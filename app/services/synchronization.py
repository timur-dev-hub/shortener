from app.cache.cache import redis_cache
from app.db.crud.url import upd_click_by_short_code

from app.db.database import async_session

async def redis_clicks_synchronization():
    cursor, clicks_count = await redis_cache.get_clicks_by_cursor()

    while cursor != 0:
        data = await redis_cache.get_clicks_by_cursor(cursor=cursor)
        clicks_count += data[1]
        cursor = data[0]

    clicks = {}

    for i in clicks_count:
        clicks.update(i)

    if not clicks:
        return

    async with async_session() as session:
        await upd_click_by_short_code(session, clicks)
