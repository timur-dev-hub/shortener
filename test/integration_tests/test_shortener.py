import pytest

from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, status_code",
    [
        ({"target_url": "http://test.com"}, 201),
        ({"target_url": ""}, 422),
        ({"target_url": "test@test.com"}, 422),
    ]
)
async def test_create_short_url(payload: dict, status_code: int):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:

        res = await client.post("/api/v1/short_url", json=payload)
        assert res.status_code == status_code


@pytest.mark.asyncio
async def test_get_short_urls():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        res = await client.get("/api/v1/short_url")
        assert res.status_code == 200

@pytest.mark.asyncio
async def test_delete_redirect():

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:

        create_url_res = await client.post("/api/v1/short_url", json={"target_url": "https://test-1-1-1.com"})
        assert create_url_res.status_code == 201

        short_code = create_url_res.json()["short_url"][-12:]

        res = await client.delete(f"/api/v1/short_url?short_code={short_code}")
        assert res.status_code == 204
