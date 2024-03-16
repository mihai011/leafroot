"""Functions for accessing aobject storage service."""

from miniopy_async import Minio

from config import config


client = Minio(
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
        if not await self.client.bucket_exists(config.minio_bucket):
            await self.client.make_bucket(config.minio_bucket)


async def get_object_storage_client():
    """Get object storage client."""
    minio_object = MyMinio(config.minio_bucket, client)
    await minio_object.make_bucket()
    yield minio_object
