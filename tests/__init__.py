"""
Datasource module for testing
"""
from app.app import app
from httpx import AsyncClient


class DataSource:
    """
    class for creating data sources on tests
    """

    def __init__(self):

        self.client = AsyncClient(app=app, base_url="http://test")
        self.headers = {}

    async def make_user(self, received_args=None):
        """
        makes a default user
        """

        args = {"username": "Test_user", "email": "test@gmail.com", "password": "test"}

        if received_args:
            args.update(received_args)

        response = await self.client.post("users/sign-up", json=args)
        assert response.status_code == 200

        response = await self.client.post("/users/login", json=args)
        response = response.json()

        self.headers[args["username"]] = {
            "Authorization": "Bearer {}".format(response["item"]["token"])
        }
