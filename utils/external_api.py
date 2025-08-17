"""External requests util functions."""

from __future__ import annotations

import typing as t
import urllib

from aiohttp import ClientSession

from cache import my_key_builder, testproof_cache
from logger import log

if t.TYPE_CHECKING:
    from data import HttpRequest


async def get_http_session() -> t.AsyncGenerator[ClientSession]:
    """Yields an async http session."""
    async with ClientSession() as session:
        yield session

    await session.close()


async def make_api_request(session: ClientSession, request: HttpRequest) -> str | None:
    """Constructs a http request to an external api and sends it."""
    method = request.method
    url = request.url
    params = request.params
    body = request.body
    headers = request.headers
    response = None

    query_url = f"{url}{urllib.parse.urlencode(params)}"

    if method == "GET":
        response = await make_get_request(session, query_url, headers)

    if method == "POST":
        response = await make_post_request(session, query_url, body, headers)

    return response


@log()
@testproof_cache(key_builder=my_key_builder)
async def make_get_request(
    session: ClientSession, url: str, headers: dict[str, str]
) -> str:
    """Makes a http request to an url with GET method.

    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url

    Returns:
    response from the external api in text form
    """
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def make_post_request(
    session: ClientSession, url: str, body: dict[str, str], headers: dict[str, str]
) -> str:
    """Makes a http request to an url with POSt method.

    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url
    body (dict):  payload for post method

    Returns:
    response from the external api in text form
    """
    async with session.post(url, json=body, headers=headers) as response:
        return await response.text()
