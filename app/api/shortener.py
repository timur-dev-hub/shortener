from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.api.dependencies import get_current_user_id, get_session
from app.schemas.schortener import LinkCreate, LinkResponse, ShortCode, UrlsResponse

from app.services.schortner import create_short_link, redirect_url, get_all_short_urls, delete_redirect_url
from app.core.exceptions import AlreadyExists, NotFound

router = APIRouter()
redirect_router = APIRouter()

@router.post("/short_url", status_code=status.HTTP_201_CREATED)
async def create_short_url(
        url_data: LinkCreate,
        database_session: AsyncSession = Depends(get_session),
        user_id: UUID = Depends(get_current_user_id)
):
    try:
        url_data = await create_short_link(database_session, url_data, user_id)
        return LinkResponse.model_validate(url_data)
    except AlreadyExists:
        raise HTTPException(500, "Error short url create")

@router.get("/short_url", status_code=status.HTTP_200_OK)
async def get_short_urls(
        database_session: AsyncSession = Depends(get_session),
        user_id: UUID = Depends(get_current_user_id)
):

    urls = await get_all_short_urls(database_session, user_id)

    return UrlsResponse.model_validate({"links": urls})


@router.delete("/short_url", status_code=status.HTTP_204_NO_CONTENT)
async def delete_redirect(
        short_code: ShortCode,
        database_session: AsyncSession = Depends(get_session),
        user_id: UUID = Depends(get_current_user_id)
):
    try:
        await delete_redirect_url(database_session, short_code, user_id)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@redirect_router.get("/{short_code}")
async def redirect(
        short_code: ShortCode,
        database_session: AsyncSession = Depends(get_session)
):

    try:
        url = await redirect_url(database_session, short_code)

        return RedirectResponse(url=url)
    except NotFound:
        return RedirectResponse(url="/")
