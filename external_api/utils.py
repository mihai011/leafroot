import urllib
from aiohttp import ClientSession

async def get_http_session():
    """
    yields an async http session
    """

    async with ClientSession() as session:
        yield session

    await session.close()

async def make_api_request(session, method, url, body, params):
    """
    Constructs a http request to an external api and send it:

    Parameters:
    session (aiohttp client session): http client session
    method (string): HTTP method used for the external api
    url (string): string that represents the url
    body (dict): content for the paylod in case of 
                POST, PUT and PATCH methods
    params (dict): query parameters for the url

    Returns:
    response from the external api in text form
    """
        
    query_url ="{}{}".format(url, urllib.parse.urlencode(params))

    if method == "GET":

        response = await make_get_request(session, query_url)

    if method == "POST":

        response = await make_post_request(session, query_url, body)

    return response



async def make_get_request(session, url):
    """
    Makes a http request to an url with GET method
    
    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url

    Returns:
    response from the external api in text form

    """

    async with session.get(url) as response:

        return await response.text()

async def make_post_request(session, url, body):
    """
    Makes a http request to an url with POSt method
    
    Parameters:
    session (aiohttp client session): http client session
    url (string): string that represents the url
    body (dict):  payload for post method

    Returns:
    response from the external api in text form

    """

    async with session.post(url, json=body) as response:

        return await response.text()