from re import M
import pyiceberg
from pyiceberg.catalog import load_catalog
from config.config import s3_endpoint, minio_access_key, minio_secret_key


def get_iceberg_catalog():
    """Get the iceberg catalog."""
    return MyIcebergCatalog()


class MyIcebergCatalog:
    def __init__(self):
        """Construct the Iceberg object."""
        self.catalog = load_catalog(
            "leafroot",
            **{
                "uri": s3_endpoint,
                "s3.endpoint": s3_endpoint,
                "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
                "s3.access-key-id": minio_access_key,
                "s3.secret-access-key": minio_secret_key,
            }
        )
