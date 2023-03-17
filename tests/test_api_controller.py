"""Module for testing api controller."""

import pytest  # pylint: disable=R0801
from aioresponses import aioresponses  # pylint: disable=R0801

from data import HttpRequest
from tests import DataSource  # pylint: disable=R0801
from tests.conftest import temp_db  # pylint: disable=R0801


@pytest.mark.asyncio
@temp_db
async def test_api(session):
    """test api request controller."""

    ds = DataSource(session)
    await ds.make_user()

    payload_api = HttpRequest(
        url="http://fake_url.com",
        body="request body",
        method="GET",
        params=dict(),
        headers=dict(),
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

    key_and_missing = {
        "url": "Url",
        "body": "Body",
        "method": "Method",
        "params": "Params",
        "headers": "Headers",
    }
