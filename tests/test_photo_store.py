"""Module for testing endpoints of a photo store."""


from pickletools import pyunicode
import py
import pytest  # pylint: disable=R0801


from tests import DataSource  # pylint: disable=R0801


@pytest.mark.asyncio
async def test_upload_photo(async_session):
    """Test upload photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()

    photo_packet = {
        "photo_body": b64_image,
        "photo_name": "test",
        "photo_type": "png",
    }

    response = await ds.client.post(
        "/photo/upload", headers=ds.headers["Test_user"], json=photo_packet
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo uploaded!",
        "item": {"photo": "test.png"},
    }


@pytest.mark.asyncio
async def test_download_photo(async_session):
    """Test download photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()
    response = await ds.client.get(
        "/api/photos/1",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo downloaded!",
        "photo_id": 1,
    }


@pytest.mark.asyncio
async def test_delete_photo(async_session):
    """Test delete photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    b64_image = ds.make_photo()
    response = await ds.client.delete(
        "/api/photos/1",
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
        "/api/photos/1/info",
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
        "/api/photos/list",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Photo list received!",
        "photo_id": 1,
    }
