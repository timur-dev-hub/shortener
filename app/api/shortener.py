from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from app.schemas.schortener import LinkCreate, LinkResponse

from app.services.schortner import create_short_link

router = APIRouter()
redirect_router = APIRouter()

@router.post("/short_url", status_code=status.HTTP_201_CREATED)
async def create_short_url(url_data: LinkCreate):
    target_url = str(url_data.target_url)

    short_url_data = await create_short_link(target_url)

    short_url = f"http://localhost:8000/{short_url_data.get("short_code")}"

    return LinkResponse(
        id=short_url_data.get("id"),
        target_url=short_url_data.get("target_url"),
        short_url=short_url,
        created_at=short_url_data.get("created_at"),
    )

@redirect_router.get("/{short_code}")
async def redirect(short_code: str):


    return RedirectResponse(url=f"http://localhost:8000/{short_code}")