import urllib
from aiohttp import ClientSession

from cache import testproof_cache


async def get_http_session():
    """
    yields an async http session
    """

    async with ClientSession() as session:
        yield session

    await session.close()


async def make_api_request(session, content):
    """
    Constructs a http request to an external api and send it:

    Parameters:
    session (aiohttp client session): http client session
    content (dict) that contains the following

        method (string): HTTP method used for the external api
        url (string): string that represents the url
        body (dict): content for the paylod in case of
                    POST, PUT and PATCH methods
        params (dict): query parameters for the url
        headers (dict): headers to be sent in request

    Returns:
    response from the external api in text form
    """

    method = content.get("method", None)
    url = content.get("url", None)
    params = content.get("params", None)
    body = content.get("body", None)
    headers = content.get("headers", None)

    query_url = "{}{}".format(url, urllib.parse.urlencode(params))

    if method == "GET":

        response = await make_get_request(session, query_url, headers)

    if method == "POST":

        response = await make_post_request(session, query_url, body, headers)

    return response


@testproof_cache(expire=1)
async def make_get_request(session, url, headers):
    """
    Makes a http request to an url with GET method

    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url

    Returns:
    response from the external api in text form

    """

    async with session.get(url, headers=headers) as response:

        return await response.text()


async def make_post_request(session, url, body, headers):
    """
    Makes a http request to an url with POSt method

    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url
    body (dict):  payload for post method

    Returns:
    response from the external api in text form

    """

    async with session.post(url, json=body, headers=headers) as response:

        return await response.text()
