from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User


async def create_user(session: AsyncSession, user: User) -> User:

    session.add(user)
    await session.commit()
    return user

async def get_user_by_email(session: AsyncSession, email: str) -> User:

    stmt = select(User).where(User.email == email)

    result = await session.execute(stmt)
    return result.scalars().one_or_none()
