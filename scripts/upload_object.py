"""
python3 upload_objects.py 
location_live.json 
https://api.develop.wisor.me/locations  
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mzc4Njg1ODgsImlhdCI6MTYzNzYwOTM4OCwic3ViIjo1fQ.RWmXnmGJSFQ1EE33VXpmmk_4yIgQt_G37NOEZ01DU2A
"""

import json, sys
import aiohttp
import asyncio
from tqdm.asyncio import tqdm


async def upload_object(session, object, url, headers):

    try:
        async with session.post(url, json=object, headers=headers, timeout=2000) as r:
            if r.status != 200:
                return object
            # await asyncio.sleep(5)
            return True
    except Exception as e:
        return object


async def upload_all(objects, url, headers):
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for object in objects:
                tasks.append(upload_object(session, object, url, headers))
            new_objects = []
            # responses = await asyncio.gather(*tasks, return_exceptions=True)
            for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                res = await f
                if res != True:
                    new_objects.append(res)

            if not new_objects:
                break
            else:
                print("Remaining objects:{}".format(len(new_objects)))
                objects = new_objects

        return True


if __name__ == "__main__":

    file_json = sys.argv[1]
    url = sys.argv[2]
    token = sys.argv[3]

    authorization_header = {"Authorization": "Bearer {}".format(token)}

    with open(file_json) as f:
        data = json.load(f)

    print("Total of {} objects".format(len(data)))

    responses = asyncio.run(upload_all(data, url, authorization_header))

    with open("output.log", "w+") as f:
        f.write(json.dumps(responses))
