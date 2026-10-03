import pytest_asyncio
from uuid import UUID

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

from app.main import app
from app.api.dependencies import get_session, get_current_user_id

from app.db.database import Base
from app.db.models.user import User
from app.db.models.url import Url

test_engine = create_async_engine(settings.database_url, echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000001")

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():

    assert settings.MODE == "test"

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with test_async_session() as session:
        test_user = User(
            id=TEST_USER_ID,
            username="test_user_1",
            email="test_1@example.com",
            password="hashed_password_1",
        )

        session.add(test_user)
        await session.commit()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


from app.cache import cache
from app.cache.redis_client import get_redis_client
from app.cache.cache import RedisCache
import app.services.shortener as shortener

@pytest_asyncio.fixture(autouse=True)
async def setup_redis():
    client = get_redis_client()
    new_redis_cache = RedisCache(client)

    cache.redis_cache = new_redis_cache
    shortener.redis_cache = new_redis_cache

    yield

    await client.aclose()

async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session



async def override_get_current_user_id() -> UUID:
    return TEST_USER_ID

app.dependency_overrides[get_current_user_id] = override_get_current_user_id