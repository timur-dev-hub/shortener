from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import security
from app.schemas.user import UserRegister, UserLogin, UserResponse

from app.services.auth import register_user, login_user
from app.api.dependencies import get_session

from app.core.exceptions import InvalidUserData, AlreadyExists


router = APIRouter()

@router.post("/registration", status_code=status.HTTP_200_OK)
async def registration(
        register_data: UserRegister,
        response: Response,
        database_session: AsyncSession = Depends(get_session)
):
    try:
        user = await register_user(database_session, register_data)
        token = security.create_access_token(str(user.id))
        security.set_access_cookies(token, response)

        return UserResponse.model_validate(user)
    except AlreadyExists:
        raise HTTPException(status_code=409, detail="Unable to create account")

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
        login_data: UserLogin,
        response: Response,
        database_session: AsyncSession = Depends(get_session)
):
    try:
        user = await login_user(database_session, login_data)
        token = security.create_access_token(str(user.id))
        security.set_access_cookies(token, response)

        return UserResponse.model_validate(user)
    except InvalidUserData:
        raise HTTPException(status_code=401, detail="Incorrect username or password")


