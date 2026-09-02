import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI


from app.workers.clicks import clicks_synchronization
from app.core.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):

    setup_logging()
    logger = logging.getLogger(__name__)

    task = asyncio.create_task(clicks_synchronization())
    logger.info("App started")

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    logger.info("App ended")