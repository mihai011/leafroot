"""Module for testing api controller."""

import pytest  # pylint: disable=R0801
from aioresponses import aioresponses  # pylint: disable=R0801

from data import HttpRequest
from tests import DataSource  # pylint: disable=R0801


@pytest.mark.asyncio
async def test_api(async_session):
    """Test api request controller."""

    ds = DataSource(async_session)
    await ds.make_user()

    payload_api = HttpRequest(
        url="http://fake_url.com",
        body="request body",
        method="GET",
        params={},
        headers=(),
    )
    with aioresponses() as mocked:
        mocked.get(payload_api.url, status=200, body="test1")
        response = await ds.client.post(
            "/api/external",
            data=payload_api.json(),
            headers=ds.headers["Test_user"],
        )
    assert response.status_code == 200
    assert response.json() == {
        "message": "api called",
        "item": "test1",
        "status": 200,
    }
