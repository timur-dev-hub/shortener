from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.schemas.user import UserRegister, UserLogin
from app.db.models.user import User
from app.db.crud.user import create_user, get_user_by_email

from app.core.exceptions import InvalidUserData, AlreadyExists


password_hash = PasswordHash.recommended()


async def get_hashed_password(password: str) -> PasswordHash:
    return password_hash.hash(password)

async def register_user(
    session: AsyncSession,
    data: UserRegister
):

    hashed_password = await get_hashed_password(data.password)
    data_user = User(
        username=data.username,
        password=hashed_password,
        email=data.email,

    )

    try:
        user = await create_user(session, data_user)
        return user
    except IntegrityError:
        raise AlreadyExists


async def login_user(
    session: AsyncSession,
    input_data: UserLogin
):
    email = input_data.email

    user = await get_user_by_email(session, email)

    if not user:
        raise InvalidUserData

    if password_hash.verify(input_data.password, user.password):
        return user
    else:
        raise InvalidUserData
