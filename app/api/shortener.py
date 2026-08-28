from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.api.dependencies import get_current_user_id, get_session
from app.schemas.schortener import LinkCreate, LinkResponse, ShortCode

from app.services.schortner import create_short_link, redirect_url


router = APIRouter()
redirect_router = APIRouter()

@router.post("/short_url", status_code=status.HTTP_201_CREATED)
async def create_short_url(
        url_data: LinkCreate,
        database_session: AsyncSession = Depends(get_session),
        user_id: UUID = Depends(get_current_user_id)
):

    url_data = await create_short_link(database_session, url_data, user_id)
    return LinkResponse.model_validate(url_data)


@redirect_router.get("/{short_code}")
async def redirect(
        short_code: ShortCode,
        database_session: AsyncSession = Depends(get_session)
):

    url = await redirect_url(database_session, short_code)

    return RedirectResponse(url=url.target_url)
