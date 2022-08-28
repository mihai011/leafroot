"""Datasource module for testing."""
from httpx import AsyncClient

from app.app import app
from data import User


class DataSource:
    """Class for creating data sources on tests."""

    def __init__(self, session):
        """Datasource class constructor."""
        self.client = AsyncClient(app=app, base_url="http://test")
        self.headers = {}
        self.session = session

    async def make_user(self, received_args=None):
        """Make a default user."""
        args = {"username": "Test_user", "email": "test@gmail.com", "password": "test"}

        if received_args:
            args.update(received_args)

        response = await self.client.post("users/sign-up", json=args)
        assert response.status_code == 200

        user = await User.GetById(self.session, 1)
        assert str(user) == "<User 'Test_user'>"

        response = await self.client.post("/users/login", json=args)
        response = response.json()

        self.headers[args["username"]] = {
            "Authorization": "Bearer {}".format(response["item"]["token"])
        }
