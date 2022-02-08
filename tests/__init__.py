"""
Datasource module for testing
"""
from fastapi.testclient import TestClient
from app.app import app


class DataSource:
    """
    class for creating data sources on tests
    """

    def __init__(self):

        self.client = TestClient(app)
        args = {"username": "Test_user", "email": "test@gmail.com", "password": "test"}

        response = self.client.post("users/sign-up", json=args)
        assert response.status_code == 200

        args = {
            "username": "Test_user",
            "password": "test",
            "email": "test@gmail.com",
        }

        response = self.client.post("/users/login", json=args)
        response = response.json()

        self.headers = {"Authorization": "Bearer {}".format(response["item"]["token"])}
