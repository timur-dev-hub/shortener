from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.api.dependencies import get_current_user_id, get_session
from app.schemas.schortener import LinkCreate

from app.services.schortner import create_short_link


router = APIRouter()
redirect_router = APIRouter()

@router.post("/short_url", status_code=status.HTTP_201_CREATED)
async def create_short_url(
        url_data: LinkCreate,
        database_session: AsyncSession = Depends(get_session),
        user_id: UUID = Depends(get_current_user_id)
):

    await create_short_link(database_session, url_data, user_id)
    return {"user_id": user_id, "url": url_data.target_url}


@redirect_router.get("/{short_code}")
async def redirect(short_code: str):

    return RedirectResponse(url=f"http://localhost:8000/{short_code}")
