"""Module for testing endpoints of a photo store."""


import pytest  # pylint: disable=R0801

from tests import DataSource  # pylint: disable=R0801
from utils import is_valid_uuid


@pytest.mark.asyncio
async def test_upload_photo(async_session):
    """Test upload photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    images_bytes = ds.make_photo((2048, 2048, 3))

    response = await ds.client.post(
        "/photo/upload",
        headers=ds.headers["Test_user"],
        files={"file": ("test.png", images_bytes, "image/png")},
    )
    assert response.status_code == 200
    assert "photo_id" in response.json()["item"]
    assert is_valid_uuid(response.json()["item"]["photo_id"])


@pytest.mark.asyncio
async def test_download_photo(async_session):
    """Test download photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    NUMBER_OF_UPLOADS = 10
    list_ids = await ds.make_uploads_for_user(
        ds.headers["Test_user"], NUMBER_OF_UPLOADS
    )

    for photo_id in list_ids:
        response = await ds.client.get(
            f"/photo/download/{photo_id}",
            headers=ds.headers["Test_user"],
        )
        assert response.status_code == 200
