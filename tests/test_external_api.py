"""Tests for external call functions."""

import aiohttp
from aioresponses import aioresponses
from fastapi import status

from data import HttpRequest
from utils.external_api import (
    make_api_request,
    make_get_request,
    make_post_request,
)


async def test_make_get_request() -> None:
    """Tests for a make-get_request."""
    url_test = "http://fake_url.com"
    session = aiohttp.ClientSession()
    headers = {}
    with aioresponses() as mocked:
        mocked.get(url_test, status=status.HTTP_200_OK, body="test1")
        response = await make_get_request(session, url_test, headers)
        assert response == "test1"
    await session.close()


async def test_make_post_request() -> None:
    """Tests for a make-get_request."""
    url_test = "http://fake_url.com"
    session = aiohttp.ClientSession()
    headers = {}
    body = {}
    with aioresponses() as mocked:
        mocked.post(url_test, status=200, body="test1")
        response = await make_post_request(session, url_test, body, headers)
        assert response == "test1"
    await session.close()


async def test_get_request_external() -> None:
    """Test a simple request to a fake api service."""
    url_test = "http://fake_url.com"

    content = HttpRequest(
        url="http://fake_url.com",
        body="",
        method="GET",
        params={},
        headers={},
    )

    session = aiohttp.ClientSession()

    with aioresponses() as mocked:
        mocked.get(url_test, status=200, body="test1")
        response = await make_api_request(session, content)
        assert response == "test1"

    with aioresponses() as mocked:
        mocked.post(url_test, status=200, body="test2")
        content.method = "POST"
        response = await make_api_request(session, content)
        assert response == "test2"

    with aioresponses() as mocked:
        mocked.post(url_test, status=200, body="test3")
        content.body = "{'data': 'test_data'}"
        content.method = "POST"
        response = await make_api_request(session, content)
        assert response == "test3"

    await session.close()
