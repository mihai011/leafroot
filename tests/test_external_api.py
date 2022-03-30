"""
tests for external call functions
"""
import aiohttp
import pytest
from aioresponses import aioresponses


from external_api.utils import make_api_request


@pytest.mark.asyncio
async def test_get_request_external():
    """
    test a simple request to a fake api service
    """
    url_test = "http://fake_url.com"

    with aioresponses() as mocked:
        mocked.get(url_test, status=200, body="test1")
        session = aiohttp.ClientSession()
        response = await make_api_request(
            session, "GET", "http://fake_url.com", None, {}
        )

        assert response == "test1"

    with aioresponses() as mocked:
        mocked.post(url_test, status=200, body="test2")
        session = aiohttp.ClientSession()
        response = await make_api_request(
            session, "POST", "http://fake_url.com", None, {}
        )
        assert response == "test2"

    with aioresponses() as mocked:
        mocked.post(url_test, status=200, body="test3")
        session = aiohttp.ClientSession()
        payload = {"data": "test_data"}
        response = await make_api_request(
            session, "POST", "http://fake_url.com", payload, {}
        )
        assert response == "test3"
