from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from uuid import UUID

from app.db.models.url import Url

from app.schemas.schortener import ShortCode


async def create_entry_short_url(session: AsyncSession, url: Url) -> Url:
    session.add(url)
    try:
        await session.commit()
        return url
    except IntegrityError:
        await session.rollback()
        raise

async def check_exist_target_url(session: AsyncSession, user_id: UUID, target_url: str) -> Url | None:
    stmt = select(Url).where(Url.user_id == user_id).where(Url.target_url == target_url)
    result = await session.execute(stmt)

    return result.scalars().one_or_none()



async def get_target_url_by_short_code(session: AsyncSession, short_code: ShortCode) -> Url:
    stmt = select(Url).where(Url.short_code == short_code)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()

async def get_all_short_urls_by_user_id(session: AsyncSession, user_id: UUID) -> list[Url]:
    stmt = select(Url).where(Url.user_id == user_id)

    result = await session.execute(stmt)

    return result.scalars().all()

