import asyncio

from app.services.synchronization import redis_clicks_synchronization

async def clicks_synchronization():
    while True:
        await redis_clicks_synchronization()
        await asyncio.sleep(600)



