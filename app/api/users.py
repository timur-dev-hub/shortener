from fastapi import APIRouter, Response, Depends, status

from app.core.security import security
from app.schemas.user import UserRegister, UserLogin, UserResponse

from app.services.auth import register_user
from app.api.dependencies import get_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(
        register_data: UserRegister,
        response: Response,
        database_session: AsyncSession = Depends(get_session)
):
    user = await register_user(database_session, register_data)
    token = security.create_access_token(str(user.id))
    security.set_access_cookies(token, response)

    return UserResponse.model_validate(user)

@router.get("/login")
async def login(login_data: UserLogin):

    return {"massage": "login TRUE"}
