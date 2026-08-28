import random
import string
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.db.models.url import Url
from app.db.crud.url import create_entry_short_url
from app.schemas.schortener import LinkCreate

from app.core.exceptions import InvalidUserData


async def generate_code(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


async def create_short_link(session: AsyncSession, link: LinkCreate, user_id: UUID) -> Url:

    short_code = await generate_code()


    url = Url(
        user_id=user_id,
        target_url=str(link.target_url),
        short_code=short_code
    )


    return await create_entry_short_url(session, url)




