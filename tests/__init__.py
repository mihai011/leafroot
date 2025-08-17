"""Datasource module for testing."""

from __future__ import annotations

import typing as t
from io import BytesIO

import numpy as np
from PIL import Image
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from tqdm import tqdm

from app.app import app
from data import User
from utils import random_string

if t.TYPE_CHECKING:
    from numpy.typing import NDArray
    from sqlalchemy import Session

HTTP_STATUS_CODE = status.HTTP_200_OK


class DataSource:
    """Class for creating data sources on tests."""

    def __init__(self, session: Session) -> None:
        """Datasource class constructor."""
        self.client = AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        )
        self.test_client = TestClient(app=app, base_url="http://test")
        self.headers = {}
        self.session = session

    async def make_users(self, number_of_users: int) -> bool:
        """Create users susing the faker package."""
        f = Faker(["it_IT", "en_US", "ja_JP"])
        for _ in tqdm(range(number_of_users)):
            args = {
                "username": f.name() + random_string(),
                "email": f.email() + random_string(),
                "hashed_pass": f.password(),
                "address": f.address(),
            }

            await User.add_new(self.session, args)

        return True

    async def make_user(self, received_args: dict | None = None) -> tuple(dict, int):
        """Make a default user."""
        args = {
            "username": "Test_user",
            "email": "test@gmail.com",
            "password": "test",
            "permissions": "110",
        }

        if received_args is not None:
            args.update(received_args)

        response = await self.client.post("users/sign-up", json=args)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        user_id = response["item"]["id"]

        user = await User.get_by_id(self.session, user_id)
        username = args["username"]
        assert str(user) == f"<User {username}>"

        response = await self.client.post("/users/login", json=args)
        response = response.json()

        header = {"Authorization": "Bearer {}".format(response["item"]["token"])}
        user_id = response["item"]["user"]["id"]

        self.headers[username] = header

        return header, user_id

    def make_photo(self, dims: tuple = (256, 256, 3)) -> bytes:
        """Make a photo."""
        # Create the random number generator
        rng = np.random.default_rng(seed=42)

        # Image dimensions: height x width x channels
        height, width, channels = dims

        # Generate random pixel values (0 to 255) as uint8
        image: NDArray[np.uint8] = rng.integers(
            low=0, high=256, size=(height, width, channels), dtype=np.uint8
        )

        # Convert the numpy array to a PIL image
        image = Image.fromarray(image)

        # Create a BytesIO object and save the image to it
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")

        # Move the cursor to the beginning of the file
        image_bytes.seek(0)

        return image_bytes

    async def make_photo_uploads_for_user(
        self, user_header: dict, number_of_uploads: int
    ) -> list[int]:
        """Make uploads for user."""
        list_ids = []
        for _ in range(number_of_uploads):
            image_bytes = self.make_photo()

            response = await self.client.post(
                "/photo/upload",
                headers=user_header,
                files={"file": ("test.png", image_bytes, "image/png")},
            )
            assert response.status_code == status.HTTP_200_OK
            list_ids.append(response.json()["item"]["photo_id"])

        return list_ids
