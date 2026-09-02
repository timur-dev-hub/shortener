import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.schemas.user import UserRegister, UserLogin
from app.db.models.user import User
from app.db.crud.user import create_user, get_user_by_email

from app.core.exceptions import InvalidUserData, AlreadyExists

logger = logging.getLogger(__name__)
password_hash = PasswordHash.recommended()


async def register_user(
    session: AsyncSession,
    data: UserRegister
):

    hashed_password = password_hash.hash(data.password)
    data_user = User(
        username=data.username,
        password=hashed_password,
        email=data.email,

    )

    try:
        user = await create_user(session, data_user)
        logger.info(f"Created new user")
        return user
    except IntegrityError:
        logger.info(f"User already exists")
        raise AlreadyExists


async def login_user(
    session: AsyncSession,
    input_data: UserLogin
):
    email = input_data.email

    user = await get_user_by_email(session, email)

    if not user:
        logger.info(f"User login failed")
        raise InvalidUserData

    if password_hash.verify(input_data.password, user.password):
        logger.info("User logged in")
        return user
    else:
        logger.info("User login failed")
        raise InvalidUserData
