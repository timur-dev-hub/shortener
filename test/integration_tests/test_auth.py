import pytest

from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, status_code",
    [
        ({"username": "test", "email": "test@test.com", "password": "asfknpakwms"}, 201),
        ({"username": "test", "email": "test@test.com", "password": "asfknpakwms"}, 409),
        ({"username": "test", "email": "", "password": ""}, 422),
     ]
)
async def test_registration(payload: dict, status_code: int):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:


        res = await client.post("/api/v1/auth/registration", json=payload)
        assert res.status_code == status_code
