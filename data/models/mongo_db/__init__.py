"""
Models for mongodb database
"""

import motor.motor_asyncio

from config import config


async def get_mongo_client():
    """Creates mongo client"""
    client_auth = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_url_auth)
    client_not_auth = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_not_auth
    )

    try:
        await client_auth.server_info()
        yield client_auth
    except:
        yield client_not_auth


class BaseMongo:
    """Base class for mongo models"""

    collection__name = "base"

    @classmethod
    async def GetItemById(cls, db, item_id):
        """Get Item by id  field"""
        collection = db[cls.collection__name]
        res = await collection.find_one({"id": item_id})
        return res

    @classmethod
    async def AddItem(cls, db, item) -> bool:
        """Add a book to library"""
        collection = db[cls.collection__name]
        data = item.dict()
        data["id"] = str(data["id"])
        res = await collection.insert_one(data)
        return res.acknowledged
