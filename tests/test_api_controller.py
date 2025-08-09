"""Module for testing api controller."""

from aioresponses import aioresponses  # pylint: disable=R0801
from fastapi import status

from data import HttpRequest
from tests import DataSource  # pylint: disable=R0801


async def test_api(async_session):
    """Test api request controller."""

    ds = DataSource(async_session)
    await ds.make_user()

    payload_api = HttpRequest(
        url="http://fake_url.com",
        body="request body",
        method="GET",
        params={},
        headers={},
    )
    with aioresponses() as mocked:
        mocked.get(str(payload_api.url), status=200, body="test1")
        response = await ds.client.post(
            "/api/external",
            data=payload_api.json(),
            headers=ds.headers["Test_user"],
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Api called",
        "item": "test1",
    }
