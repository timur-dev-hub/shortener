from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegister
from app.db.models.user import User
from app.db.crud.user import create_user

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

async def register_user(
    session: AsyncSession,
    data: UserRegister
):

    hashed_password = password_hash.hash(data.password)
    user = User(
        username=data.username,
        password=hashed_password,
        email=data.email,

    )

    return await create_user(session, user)
