import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.workers.clicks import clicks_synchronization

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app started")
    task = asyncio.create_task(clicks_synchronization())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    print("app ended")