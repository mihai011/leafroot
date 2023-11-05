"""Test short url feature"""

from fastapi import status
import pytest

from tests import DataSource


@pytest.mark.asyncio
async def test_url_status(async_session):
    """Test url shortner"""

    ds = DataSource(async_session)
    await ds.make_user()
    url_package = {"url": "http://test.com"}
    response = await ds.client.post(
        "/url-short/set", json=url_package, headers=ds.headers["Test_user"]
    )

    assert response.status_code == status.HTTP_200_OK
    url_response = response.json()
    assert url_response["message"] == "Url made!"
    short_url = url_response["item"]["url"]
    response = await ds.client.get(
        short_url,
        headers=ds.headers["Test_user"],
    )

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    url_response = response.json()
    assert url_response["item"]["url"] == url_package["url"]

    url_package = {"url": "http:/wrong_url.com"}
    response = await ds.client.post(
        "/url-short/set", json=url_package, headers=ds.headers["Test_user"]
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
