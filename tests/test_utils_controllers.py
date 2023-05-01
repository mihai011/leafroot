"""Testing the health check."""

import json

import pytest

from tests import DataSource


@pytest.mark.asyncio
async def test_health_status(async_session):
    """Verifying the health check."""

    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.get(
        "/utils/health_check", headers=ds.headers["Test_user"]
    )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    health_check_ok = {
        "postgressql": True,
        "redis": True,
        "rabbitmq": True,
        "mongo": True,
    }
    assert response_data["item"] == health_check_ok


@pytest.mark.asyncio
async def test_quotes(async_session):
    """Verifying the quotes endpoint."""

    ds = DataSource(async_session)
    await ds.make_user()

    payload_quote = {"quote": "test", "author": "author"}

    response = await ds.client.post(
        "/utils/quote", headers=ds.headers["Test_user"], json=payload_quote
    )
    assert response.status_code == 200
    response = await ds.client.get(
        "/utils/quote", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data["item"]["quote"] == payload_quote["quote"]
