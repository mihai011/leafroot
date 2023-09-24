"""Datasource module for testing."""
from tqdm import tqdm
from faker import Faker
from httpx import AsyncClient
from fastapi import status
from fastapi.testclient import TestClient

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
