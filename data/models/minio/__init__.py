"""Functions for accessing aobject storage service."""

from miniopy_async import Minio

from config import config
import io


class MinioObject(Minio):
    """Class for minio object, implements with singleton design pattern"""

    _instance = None

    @classmethod
    async def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls(
                config.minio_endpoint,
                config.minio_root_user,
                config.minio_root_password,
                secure=config.minio_secure,
            )

        if not await cls._instance.bucket_exists(config.minio_bucket):
            await cls._instance.make_bucket(config.minio_bucket)

        return cls._instance

    def __init__(self, *args, **kwargs):
        if self._instance is not None:
            raise Exception("This class is a singleton!")

        super().__init__(*args, **kwargs)


async def get_object_storage_client():
    """Get object storage client."""
    client = await MinioObject.getInstance()
    yield client
