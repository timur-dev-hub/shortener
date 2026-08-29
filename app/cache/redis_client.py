from redis.asyncio import Redis

from app.core.config import settings

client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
