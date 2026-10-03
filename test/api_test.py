import pytest
from httpx import AsyncClient, ASGITransport

from app.schemas.user import UserResponse
from app.main import app


password="mytestpostgres"

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:

        res = await client.get("/health")

        assert res.status_code == 200

        assert res.json() == {"status": "ok", "version": "1.0.0"}


@pytest.mark.asyncio
async def test_registration():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:

        res = await client.post("/registration", json={"username": "test", "password": "asfknpakwms"})

        assert res.status_code == 201
        assert UserResponse.model_validate(res.json())

        res = await client.post("/registration", json={"username": "", "password": ""})

        assert res.status_code == 422
