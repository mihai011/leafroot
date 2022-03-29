"""
tests for external call functions
"""
import aiohttp
import pytest


from external_api.utils import make_api_request
from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_get_request_external():
    """
    test a simple request to a fake api service
    """

    with aioresponses() as mocked:
        mocked.get("http://fake_url.com", status=200, body="test")
        session = aiohttp.ClientSession()
        response = await make_api_request(
            session, "GET", "http://fake_url.com", None, {}
        )

        assert response == "test"

    with aioresponses() as mocked:
        mocked.post("http://fake_url.com", status=200, body="test")
        session = aiohttp.ClientSession()
        response = await make_api_request(
            session, "POST", "http://fake_url.com", None, {}
        )

        assert response == "test"
