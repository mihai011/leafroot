"""Python3 time test controllers."""

import json
import sys
import asyncio
import aiohttp
from tqdm.asyncio import tqdm


async def make_call(session, url):

    async with session.get(url) as r:
        return r


async def async_calls(url, reqs):

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(reqs):
            tasks.append(make_call(session, url))
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            res = await task


if __name__ == "__main__":

    reqs = int(sys.argv[1])

    url_sync = "http://localhost/sync_controller"
    url_async = "http://localhost/async_controller"

    responses = asyncio.run(async_calls(url_async, reqs))
    responses = asyncio.run(async_calls(url_sync, reqs))

    with open("output.log", "w+", encoding="utf-8") as f:
        f.write(json.dumps(responses))
