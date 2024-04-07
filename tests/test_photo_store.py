"""Module for testing endpoints of a photo store."""


import pytest  # pylint: disable=R0801

from tests import DataSource  # pylint: disable=R0801
from utils import is_valid_uuid


@pytest.mark.asyncio
async def test_upload_photo(async_session, minio_storage):
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
async def test_download_photo(async_session, minio_storage):
    """Test download photo."""
    ds = DataSource(async_session)
    _, user_id = await ds.make_user()
    NUMBER_OF_UPLOADS = 10
    list_ids = await ds.make_photo_uploads_for_user(
        ds.headers["Test_user"], NUMBER_OF_UPLOADS
    )

    for photo_id in list_ids:
        response = await ds.client.get(
            f"/photo/download/{photo_id}",
            headers=ds.headers["Test_user"],
        )
        assert response.status_code == 200

    response = await ds.client.get(
        f"/photo/list/{user_id}", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200

    photo_list = response.json()["item"]
    assert len(photo_list) == NUMBER_OF_UPLOADS


async def test_delete_photo(async_session, minio_storage):
    """Test delete photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    NUMBER_OF_UPLOADS = 10
    list_ids = await ds.make_photo_uploads_for_user(
        ds.headers["Test_user"], NUMBER_OF_UPLOADS
    )
    for photo_id in list_ids:
        response = await ds.client.delete(
            f"/photo/delete/{photo_id}",
            headers=ds.headers["Test_user"],
        )
        assert response.status_code == 200


async def test_follower(async_session, minio_storage):
    """Test user follower"""

    ds = DataSource(async_session)
    username_1 = "Alice"
    alice_email = "alice@gmail.com"
    alice_header, alice_id = await ds.make_user(
        {"username": username_1, "email": alice_email}
    )
    username_2 = "Bob"
    bob_email = "bob@gmail.com"

    bob_header, bob_id = await ds.make_user(
        {"username": username_2, "email": bob_email}
    )

    alice_image = ds.make_photo((2048, 2048, 3))
    response = await ds.client.post(
        "/photo/upload",
        headers=alice_header,
        files={"file": ("alice.png", alice_image, "image/png")},
    )
    assert response.status_code == 200
    alice_image_id = response.json()["item"]["photo_id"]

    bob_image = ds.make_photo((2048, 2048, 3))
    response = await ds.client.post(
        "/photo/upload",
        headers=bob_header,
        files={"file": ("bob.png", bob_image, "image/png")},
    )
    assert response.status_code == 200
    bob_image_id = response.json()["item"]["photo_id"]

    response = await ds.client.get(
        f"/photo/list/{bob_id}", headers=alice_header
    )
    assert response.status_code == 400

    response = await ds.client.post(
        f"/photo/follow/{bob_id}", headers=alice_header, json={}
    )
    assert response.status_code == 200
    response = await ds.client.post(
        f"/photo/follow/{bob_id}", headers=alice_header, json={}
    )
    assert response.status_code == 400

    response = await ds.client.get(
        f"/photo/list/{bob_id}", headers=alice_header
    )
    assert response.status_code == 200
    assert len(response.json()["item"]) == 1
    assert response.json()["item"][0]["photo_id"] == bob_image_id
