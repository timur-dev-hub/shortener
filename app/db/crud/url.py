from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.url import Url


async def create_entry_short_url(session: AsyncSession, url: Url) -> Url:
    session.add(url)
    await session.commit()
    return url