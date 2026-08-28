from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.models.url import Url

from app.schemas.schortener import ShortCode


async def create_entry_short_url(session: AsyncSession, url: Url) -> Url:
    session.add(url)
    await session.commit()
    return url

async def get_target_url_by_short_code(session: AsyncSession, short_code: ShortCode) -> Url:
    stmt = select(Url).where(Url.short_code == short_code)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()

async def get_all_short_urls_by_user_id(session: AsyncSession, user_id: UUID) -> list[Url]:
    stmt = select(Url).where(Url.user_id == user_id)

    result = await session.execute(stmt)

    return result.scalars().all()
