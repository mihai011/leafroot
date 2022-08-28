"""Some docstring."""

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def login(self):
        self.client.post(
            "http://localhost:8001/users/login",
            json={"email": "a@gmail.com", "username": "mika", "password": "control"},
        )
