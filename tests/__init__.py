"""Datasource module for testing."""
import base64

from tqdm import tqdm
from faker import Faker
from httpx import AsyncClient
from fastapi import status
from fastapi.testclient import TestClient
from PIL import Image
import numpy as np
from io import BytesIO


from app.app import app
from data import User
from utils import random_string


class DataSource:
    """Class for creating data sources on tests."""

    def __init__(self, session):
        """Datasource class constructor."""
        self.client = AsyncClient(app=app, base_url="http://test")
        self.test_client = TestClient(app=app, base_url="http://test")
        self.headers = {}
        self.session = session

    async def make_users(self, number_of_users):
        """Create users susing the faker package."""

        f = Faker(["it_IT", "en_US", "ja_JP"])
        for _ in tqdm(range(number_of_users)):
            args = {
                "username": f.name() + random_string(),
                "email": f.email() + random_string(),
                "hashed_pass": f.password(),
                "address": f.address(),
            }

            await User.AddNew(self.session, args)

        return True

    async def make_user(self, received_args=None):
        """Make a default user."""
        args = {
            "username": "Test_user",
            "email": "test@gmail.com",
            "password": "test",
            "address": "test",
        }

        if received_args:
            args.update(received_args)

        response = await self.client.post("users/sign-up", json=args)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        user = await User.GetById(self.session, 1)
        assert str(user) == "<User 'Test_user'>"

        response = await self.client.post("/users/login", json=args)
        response = response.json()

        header = {
            "Authorization": "Bearer {}".format(response["item"]["token"])
        }

        self.headers[args["username"]] = header

        return header

    def make_photo(self, dims=(256, 256, 3)):
        """Make a photo."""

        # Create a new image with random pixel values
        random_image = np.random.randint(0, 256, dims, dtype=np.uint8)

        # Convert the numpy array to a PIL image
        image = Image.fromarray(random_image)

        # Create a BytesIO object and save the image to it
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")

        # Move the cursor to the beginning of the file
        image_bytes.seek(0)

        return image_bytes

    async def make_uploads_for_user(self, user_header, number_of_uploads):
        """Make uploads for user."""
        list_ids = []
        for _ in range(number_of_uploads):
            image_bytes = self.make_photo()

            response = await self.client.post(
                "/photo/upload",
                headers=user_header,
                files={"file": ("test.png", images_bytes, "image/png")},
            )
            assert response.status_code == 200
            assert response.json() == {
                "message": "Photo uploaded!",
                "item": {"photo": "test.png"},
            }

            list_ids.append(response.json()["item"]["photo_id"])
