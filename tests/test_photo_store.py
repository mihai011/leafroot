"""Module for testing endpoints of a photo store."""


import pytest  # pylint: disable=R0801
from io import BytesIO  # pylint: disable=R0801

from tests import DataSource  # pylint: disable=R0801


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
    assert response.json()["item"]["photo_path"].endswith("test.png")


@pytest.mark.asyncio
async def test_download_photo(async_session):
    """Test download photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    list_of_ids = await ds.upload_photos(ds.headers["Test_user"], 100)


@pytest.mark.asyncio
async def test_delete_photo(async_session):
    """Test delete photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()
    response = await ds.client.delete(
        "/photos/1",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo deleted!",
        "photo_id": 1,
    }


@pytest.mark.asyncio
async def test_get_photo_info(async_session):
    """Test get photo info."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()
    response = await ds.client.get(
        "/photos/1/info",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo info received!",
        "photo_id": 1,
    }


@pytest.mark.asyncio
async def test_get_photo_list(async_session):
    """Test get photo list."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()
    response = await ds.client.get(
        "/photos/list",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo list received!",
        "photo_id": 1,
    }
