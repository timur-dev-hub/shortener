import random
import string
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


from app.db.models.url import Url
from app.db.crud.url import create_entry_short_url, get_target_url_by_short_code, get_all_short_urls_by_user_id
from app.schemas.schortener import LinkCreate, ShortCode

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


async def redirect_url(session: AsyncSession, short_code: ShortCode) -> Url:

    url_data = await get_target_url_by_short_code(session, short_code)

    return url_data

async def get_all_short_urls(session: AsyncSession, user_id: UUID) -> list[Url]:

    all_short_urls = await get_all_short_urls_by_user_id(session, user_id)

    return all_short_urls
