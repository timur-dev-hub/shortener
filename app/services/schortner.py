import random
import string

from datetime import datetime

async def generate_code(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


async def create_short_link(target_url: str) -> dict[str, int]:

    short_code = await generate_code()
    db_link = {
        "id": 154,
        "short_code": short_code,
        "target_url": target_url,
        "created_at": datetime.now()
    }


    return db_link

