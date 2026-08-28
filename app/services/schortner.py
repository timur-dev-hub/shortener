import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.schemas.user import UserRegister, UserLogin
from app.db.models.user import User
from app.db.crud.user import create_user, get_user_by_email

from app.core.exceptions import InvalidUserData

from datetime import datetime

async def generate_code(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


async def create_short_link(session: AsyncSession, target_url: str):

    short_code = await generate_code()




