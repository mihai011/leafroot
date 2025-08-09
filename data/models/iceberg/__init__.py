from pyiceberg.catalog import load_catalog

from config import config


def get_iceberg_catalog():
    """Get the iceberg catalog."""
    return MyIcebergCatalog()


class MyIcebergCatalog:
    """Iceberg Catalog"""

    def __init__(self):
        """Construct the Iceberg object."""
        self.catalog = load_catalog(
            "leafroot",
            **{
                "uri": config.s3_endpoint,
                "s3.endpoint": config.s3_endpoint,
                "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
                "s3.access-key-id": config.minio_access_key,
                "s3.secret-access-key": config.minio_secret_key,
            },
        )
