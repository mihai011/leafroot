"""Start of the controller module."""

import string
import logging
from functools import wraps

from fastapi.responses import ORJSONResponse

from data import User
from utils import get_password_hash, authenthicate_user, random_string
from logger import log


@log()
def auth_decorator(controller):
    """Authenthication decorator, query and payload parser."""

    @wraps(controller)
    async def auth(*args, **kwargs):
        """Function that gets token and adds session to the controller."""
        request = kwargs["request"]
        session = kwargs["session"]

        if "authorization" not in request.headers:
            return create_response("Authorization header not present!", 401)

        token = request.headers["authorization"].split(" ")[-1]

        if not await authenthicate_user(token, session):
            return create_response(
                "Token expired or invalid! Please login again!", 401
            )

        response = await controller(*args, **kwargs)
        return response

    return auth


@log()
async def parse(request):
    """simple parser for request."""
    if request.method == "GET":
        args = request.query_params._dict

    if request.method == "POST":
        args = await request.json()

    return args


@log()
def create_response(message: string, status: int, item=None) -> ORJSONResponse:
    """Receive a message parameter from which a reponse is created and item
    from wich a dictionay is ORJSONResponse object is made as response."""
    data = {}
    data["message"] = message
    data["item"] = item
    data["status"] = status

    logging.info("Creating response with data:%s", str(data))
    return ORJSONResponse(content=data)


async def create_bulk_users(users, session):
    """Creates a lot of users."""
    for _ in range(users):

        args = {}
        args["email"] = "{}@{}".format(random_string(), random_string())
        args["username"] = random_string()
        args["hashed_pass"] = get_password_hash(random_string())
        await User.AddNew(session, args)
