import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.workers.clicks import clicks_synchronization

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app started")
    asyncio.create_task(clicks_synchronization())

    yield

    print("app ended")