"""Functions for accessing aobject storage service."""

from io import BytesIO

from aiohttp import ClientSession
from minio.helpers import ObjectWriteResult
from miniopy_async import Minio
from miniopy_async.deleteobjects import DeleteObject
from urllib3.response import HTTPResponse

from cache import my_key_builder, testproof_cache
from config import config


class MyMinio:
    """Custom class for Minio client."""

    def __init__(self, bucket: str, client: Minio) -> None:
        """Constructor for minio client."""
        self.bucket = bucket
        self.client = client

    async def put_object(
        self, object_name: str, file: BytesIO, length: int, content_type: str
    ) -> ObjectWriteResult:
        """Put object method."""
        return await self.client.put_object(
            self.bucket,
            object_name,
            file,
            length,
            content_type,
        )

    @testproof_cache(key_builder=my_key_builder)
    async def get_object(
        self, object_name: str, http_session: ClientSession
    ) -> HTTPResponse:
        """Get object method."""
        return await self.client.get_object(self.bucket, object_name, http_session)

    async def list_objects(self) -> list:
        """List objects method."""
        return await self.client.list_objects(self.bucket)

    async def make_bucket(self) -> None:
        """Make bucket method."""
        if not await self.client.bucket_exists(self.bucket):
            await self.client.make_bucket(self.bucket)

    async def remove_object(self, object_path: str) -> None:
        """Remove object method."""
        await self.client.remove_object(self.bucket, object_path)

    async def remove_bucket(self) -> None:
        """Remove bucket method."""
        files = await self.client.list_objects(self.bucket, recursive=True)
        delete_objects = [DeleteObject(file.object_name) for file in files]

        await self.client.remove_objects(self.bucket, delete_objects)
        await self.client.remove_bucket(self.bucket)


def get_minio_client() -> Minio:
    """Create minio client."""
    return Minio(
        config.minio_url,
        access_key=config.minio_root_user,
        secret_key=config.minio_root_password,
        secure=config.minio_secure,
    )


async def get_object_storage_client() -> MyMinio:
    """Get object storage client."""
    minio_client = get_minio_client()
    minio_object = MyMinio(config.minio_bucket, minio_client)
    await minio_object.make_bucket()
    yield minio_object
