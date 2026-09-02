import random
import string
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from app.db.models.url import Url
from app.db.crud.url import (create_entry_short_url, get_target_url_by_short_code,
                             get_all_short_urls_by_user_id, check_exist_target_url,
                             delete_entry_short_url)

from app.cache.cache import redis_cache

from app.schemas.shortener import LinkCreate, ShortCode
from app.core.exceptions import AlreadyExists, NotFound

logger = logging.getLogger(__name__)

def generate_code(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


async def create_short_link(session: AsyncSession, link: LinkCreate, user_id: UUID) -> Url:
    target_url = str(link.target_url)

    short_url = await check_exist_target_url(session, user_id, target_url)

    if short_url:
        return short_url

    for _ in range(10):

        short_code = generate_code()

        try:
            url = Url(
                user_id=user_id,
                target_url=target_url,
                short_code=short_code
            )
            short_url_entry = await create_entry_short_url(session, url)
            logger.info(f"User: {user_id} creating short url | target: {target_url} short_code: {short_url}")
            return short_url_entry

        except IntegrityError:
            logger.warning("A collision occurred while creating the short code")
            continue
    logger.error("10 consecutive collisions occurred while generating a short code")
    raise AlreadyExists

async def redirect_url(session: AsyncSession, short_code: ShortCode) -> str:

    url = await redis_cache.get_url(short_code)
    if url:
        return url

    url_data = await get_target_url_by_short_code(session, short_code)
    if not url_data:
        raise NotFound

    await redis_cache.set_url(short_code, url_data.target_url)
    logger.info(f"Redirecting to short code {short_code}")
    return url_data.target_url


async def get_all_short_urls(session: AsyncSession, user_id: UUID) -> list[Url]:

    all_short_urls = await get_all_short_urls_by_user_id(session, user_id)
    logger.info(f"User {user_id} requested all their links")
    return all_short_urls

async def delete_redirect_url(session: AsyncSession, short_code: ShortCode, user_id: UUID) -> None:

    result = await delete_entry_short_url(session, short_code, user_id)

    await redis_cache.delete_url(short_code)
    logger.info(f"User {user_id} deleted redirect url | target: {short_code}")
    if not result:
        raise NotFound



