import pytest_asyncio

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

from app.main import app
from app.api.dependencies import get_session

from app.db.database import Base
from app.db.models.user import User
from app.db.models.url import Url

test_engine = create_async_engine(settings.database_url, echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():

    assert settings.MODE == "test"

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session