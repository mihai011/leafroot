"""Models for mongodb database."""

import motor.motor_asyncio

from config import config


async def get_mongo_client():
    """Creates mongo client."""
    client_auth = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_url_auth)
    client_not_auth = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_not_auth
    )

    try:
        await client_auth.server_info()
        yield client_auth
    except:
        yield client_not_auth


async def get_mongo_database():
    """Get mongodb database."""
    client = await anext(get_mongo_client())
    database = client[config.mongo_db]
    yield database
    client.close()


class BaseMongo:
    """Base class for mongo models."""

    collection__name = "base"

    @classmethod
    async def GetItemById(cls, db, item_id):
        """Get Item by id  field."""
        collection = db[cls.collection__name]
        res = await collection.find_one({"id": item_id}, {"_id": False})
        return res

    @classmethod
    async def DeleteItemById(cls, db, item_id):
        """Delete Item by id."""
        collection = db[cls.collection__name]
        delete_result = await collection.delete_one({"id": item_id})
        return delete_result.deleted_count

    @classmethod
    async def GetItemsByFilter(cls, db, filter_dict=None):
        """Get Items by filter, or all if filter is {}"""
        if filter_dict is None:
            filter_dict = {}
        collection = db[cls.collection__name]
        cursor = collection.find(filter_dict, {"_id": False})
        return [document async for document in cursor]

    @classmethod
    async def AddItem(cls, db, item) -> bool:
        """Add a book to library."""
        collection = db[cls.collection__name]
        data = item.dict()
        data["id"] = str(data["id"])
        res = await collection.insert_one(data)
        return res.acknowledged
