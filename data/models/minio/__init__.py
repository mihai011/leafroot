"""Functions for accessing aobject storage service."""

from http import client
from miniopy_async import Minio

from config import config
import io


class MinioObject:
    """Class for minio object, implements with singleton design pattern"""

    _instance = None

    @classmethod
    def getInstance(cls, bucket):
        if cls._instance is None:
            cls._instance = cls(bucket)
        return cls._instance

    def __init__(self, bucket):
        if self._instance is not None:
            raise RuntimeError(
                "Use getInstance() method to get the single instance of this class"
            )
        # put your MinIO connection setup code here
        self.client = Minio(
            config.minio_endpoint,
            config.minio_root_user,
            config.minio_root_password,
            secure=config.minio_secure,
        )
        self.bucket = bucket

    async def put_object(self, object_name, data):
        """Put object in minio"""
        io_data = io.BytesIO(data.encode())
        return await self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=io_data,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

    async def get_object(self, object_name):
        """Get object from minio"""
        return await self.client.get_object(self.bucket, object_name)

    async def bucket_exists(self, bucket):
        """Check if bucket exists"""
        return await self.client.bucket_exists(bucket)

    async def make_bucket(self, bucket):
        """Make bucket"""
        return await self.client.make_bucket(bucket)


async def get_object_storage_client():
    """Get object storage client."""
    client = MinioObject(config.minio_bucket)
    if not await client.bucket_exists(config.minio_bucket):
        await client.make_bucket(config.minio_bucket)
    yield client
