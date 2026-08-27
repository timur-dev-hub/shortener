from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User


async def create_user(session: AsyncSession, user: User) -> User:

    session.add(user)
    await session.commit()
    return user
