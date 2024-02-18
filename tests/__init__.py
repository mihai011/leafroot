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

        self.headers[args["username"]] = {
            "Authorization": "Bearer {}".format(response["item"]["token"])
        }

    def make_photo(self, received_args=None):
        """Make a photo."""

        # Create a new image with random pixel values
        random_image = np.random.randint(0, 256, (256, 256), dtype=np.uint8)

        # Convert the numpy array to a PIL image
        image = Image.fromarray(random_image)

        # Create a BytesIO object and save the image to it
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")

        # Move the cursor to the beginning of the file
        image_bytes.seek(0)

        # encode the image to base64
        b64image = base64.b64encode(image_bytes.read())

        return str(b64image)
