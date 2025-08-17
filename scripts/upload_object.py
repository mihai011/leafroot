# pylint: disable-all
"""Python3 upload_objects.py."""

import asyncio
import json
import sys

import Path
import aiohttp
from aiohttp import ClientSession, status
from aiohttp.web import HTTPException
from tqdm.asyncio import tqdm


async def upload_object(
    session: ClientSession, obj: dict, link: str, headers: dict
) -> bool:
    """Upload object to url."""
    try:
        async with session.post(link, json=obj, headers=headers, timeout=2000) as r:
            if r.status != status.HTTP_200_OK:
                return False
    except HTTPException:
        return False
    return True


async def upload_all(objects: list, link: str, headers: dict) -> bool:
    """Upload asynchronously all objects in the list."""
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [upload_object(session, obj, link, headers) for obj in objects]

            new_objects = []
            for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                res = await task
                if res is not True:
                    new_objects.append(res)

            if not new_objects:
                break

            print(f"Remaining objects:{len(new_objects)}")
            objects = new_objects

        return True


if __name__ == "__main__":
    file_json = sys.argv[1]
    url = sys.argv[2]
    token = sys.argv[3]

    authorization_header = {"Authorization": f"Bearer {token}"}

    with Path.open(file_json, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total of {len(data)} objects")

    responses = asyncio.run(upload_all(data, url, authorization_header))

    with Path.open("output.log", "w+", encoding="utf-8") as f:
        f.write(json.dumps(responses))
