"""Python3 upload_objects.py."""

import json
import sys
import asyncio
import aiohttp
from tqdm.asyncio import tqdm


async def upload_object(session, obj, link, headers):
    """Upload object to url."""
    try:
        async with session.post(link, json=obj, headers=headers, timeout=2000) as r:
            if r.status != 200:
                return object
            # await asyncio.sleep(5)
            return True
    except Exception:
        return object


async def upload_all(objects, link, headers):
    """Upload asynchronously all objects in the list."""
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for obj in objects:
                tasks.append(upload_object(session, obj, link, headers))
            new_objects = []
            # responses = await asyncio.gather(*tasks, return_exceptions=True)
            for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                res = await task
                if res is not True:
                    new_objects.append(res)

            if not new_objects:
                break

            print("Remaining objects:{}".format(len(new_objects)))
            objects = new_objects

        return True


if __name__ == "__main__":

    file_json = sys.argv[1]
    url = sys.argv[2]
    token = sys.argv[3]

    authorization_header = {"Authorization": "Bearer {}".format(token)}

    with open(file_json, encoding="utf-8") as f:
        data = json.load(f)

    print("Total of {} objects".format(len(data)))

    responses = asyncio.run(upload_all(data, url, authorization_header))

    with open("output.log", "w+", encoding="utf-8") as f:
        f.write(json.dumps(responses))
