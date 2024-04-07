"""Functions for accessing aobject storage service."""

import asyncio
from miniopy_async import Minio
from miniopy_async.deleteobjects import DeleteObject

from cache import testproof_cache, my_key_builder
from config import config


minio_client = Minio(
    config.minio_endpoint,
    access_key=config.minio_root_user,
    secret_key=config.minio_root_password,
    secure=config.minio_secure,
)


class MyMinio:
    def __init__(self, bucket, client):
        self.bucket = bucket
        self.client = client

    async def put_object(self, object_name, file, length, content_type):
        """Put object method."""
        return await self.client.put_object(
            self.bucket, object_name, file, length, content_type
        )

    @testproof_cache(key_builder=my_key_builder)
    async def get_object(self, object_name, http_session):
        """Get object method."""
        return await self.client.get_object(
            self.bucket, object_name, http_session
        )

    async def list_objects(self):
        """List objects method."""
        return await self.client.list_objects(self.bucket)

    async def make_bucket(self):
        """Make bucket method."""
        if not await self.client.bucket_exists(self.bucket):
            await self.client.make_bucket(self.bucket)

    async def remove_object(self, object_path):
        """Remove object method."""
        await self.client.remove_object(self.bucket, object_path)

    async def remove_bucket(self):
        """Remove bucket method."""
        files = await self.client.list_objects(self.bucket, recursive=True)
        delete_objects = [DeleteObject(file.object_name) for file in files]

        await self.client.remove_objects(self.bucket, delete_objects)
        await asyncio.sleep(1)
        await self.client.remove_bucket(self.bucket)


async def get_object_storage_client():
    """Get object storage client."""
    minio_object = MyMinio(config.minio_bucket, minio_client)
    await minio_object.make_bucket()
    yield minio_object
