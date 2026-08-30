from fastapi import Depends
from authx import TokenPayload
from uuid import UUID

from app.core.security import security

from app.db.database import async_session

async def get_session():
    async with async_session() as session:
        yield session




async def get_current_user_id(
    payload: TokenPayload = Depends(security.access_token_required),
) -> UUID:
    return UUID(payload.sub)