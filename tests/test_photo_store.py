"""Module for testing endpoints of a photo store."""

import pytest  # pylint: disable=R0801
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from data import MyMinio
from tests import DataSource  # pylint: disable=R0801
from utils import is_valid_uuid


@pytest.mark.asyncio
async def test_upload_photo(
    async_session: AsyncSession, minio_storage: MyMinio
) -> None:
    """Test upload photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    images_bytes = ds.make_photo((2048, 2048, 3))

    response = await ds.client.post(
        "/photo/upload",
        headers=ds.headers["Test_user"],
        files={"file": ("test.png", images_bytes, "image/png")},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "photo_id" in response.json()["item"]
    assert is_valid_uuid(response.json()["item"]["photo_id"])


@pytest.mark.asyncio
async def test_download_photo(
    async_session: AsyncSession, minio_storage: MyMinio
) -> None:
    """Test download photo."""
    ds = DataSource(async_session)
    _, user_id = await ds.make_user()
    number_of_uploads = 10
    list_ids = await ds.make_photo_uploads_for_user(
        ds.headers["Test_user"],
        number_of_uploads,
    )

    for photo_id in list_ids:
        response = await ds.client.get(
            f"/photo/download/{photo_id}",
            headers=ds.headers["Test_user"],
        )
        assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        f"/photo/list/{user_id}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK

    photo_list = response.json()["item"]
    assert len(photo_list) == number_of_uploads


async def test_delete_photo(
    async_session: AsyncSession, minio_storage: MyMinio
) -> None:
    """Test delete photo."""
    ds = DataSource(async_session)
    await ds.make_user()
    number_of_uploads = 10
    list_ids = await ds.make_photo_uploads_for_user(
        ds.headers["Test_user"],
        number_of_uploads,
    )
    for photo_id in list_ids:
        response = await ds.client.delete(
            f"/photo/delete/{photo_id}",
            headers=ds.headers["Test_user"],
        )
        assert response.status_code == status.HTTP_200_OK


async def test_follower(async_session: AsyncSession, minio_storage: MyMinio) -> None:
    """Test user follower."""
    ds = DataSource(async_session)
    username_1 = "Alice"
    alice_email = "alice@gmail.com"
    alice_header, alice_id = await ds.make_user(
        {"username": username_1, "email": alice_email},
    )
    username_2 = "Bob"
    bob_email = "bob@gmail.com"

    bob_header, bob_id = await ds.make_user(
        {"username": username_2, "email": bob_email},
    )

    alice_image = ds.make_photo((2048, 2048, 3))
    response = await ds.client.post(
        "/photo/upload",
        headers=alice_header,
        files={"file": ("alice.png", alice_image, "image/png")},
    )
    assert response.status_code == status.HTTP_200_OK

    bob_image = ds.make_photo((2048, 2048, 3))
    response = await ds.client.post(
        "/photo/upload",
        headers=bob_header,
        files={"file": ("bob.png", bob_image, "image/png")},
    )
    assert response.status_code == status.HTTP_200_OK
    bob_image_id = response.json()["item"]["photo_id"]

    response = await ds.client.get(f"/photo/list/{bob_id}", headers=alice_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = await ds.client.post(
        f"/photo/follow/{bob_id}",
        headers=alice_header,
        json={},
    )
    assert response.status_code == status.HTTP_200_OK
    response = await ds.client.post(
        f"/photo/follow/{bob_id}",
        headers=alice_header,
        json={},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = await ds.client.get(f"/photo/list/{bob_id}", headers=alice_header)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["item"]) == 1
    assert response.json()["item"][0]["photo_id"] == bob_image_id
