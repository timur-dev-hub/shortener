import asyncio

from app.services.synchronization import redis_clicks_synchronization

async def clicks_synchronization():
    while True:

        try:
            await asyncio.sleep(150)
        except asyncio.CancelledError:
            raise

        await redis_clicks_synchronization()
