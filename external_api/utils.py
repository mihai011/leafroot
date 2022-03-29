import urllib

async def make_api_request(session, method, url, body, params):
        
    query_url ="{}{}".format(url, urllib.parse.urlencode(params))

    if method == "GET":

        response = await make_get_request(session, query_url)

    if method == "POST":

        response = await make_post_request(session, query_url)

    return response



async def make_get_request(session, url):

    async with session.get(url) as response:

        return await response.text()

async def make_post_request(session, url):

    async with session.post(url) as response:

        return await response.text()