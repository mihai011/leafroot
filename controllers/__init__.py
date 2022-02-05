import random
import string
from functools import wraps
from fastapi.responses import ORJSONResponse

from data import User
from utils import get_password_hash, authenthicate_user


def auth_decorator(controller):

    @wraps(controller)
    async def auth(*args, **kwargs):

        token = kwargs['token']
        session = kwargs['session']

        if not await authenthicate_user(token, session):
            return create_response("Token expired! Please login again!", 401)

        return await controller(*args, **kwargs)

    return auth


def random_string():

    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(10))


def parse(request):

    if request.method == "GET":
        args = request.path_params

    if request.method == "POST":
        args = request.json()

    return args


def create_response(message: string, status:int, item=None) -> ORJSONResponse:
    """
    Receives a message parameter from which a reponse is created 
    and item from wich a dictionay is ORJSONResponse object
    is made as response 
    """

    data = {}
    data['message'] = message
    data['item'] = item
    data['status'] = status
    return ORJSONResponse(content=data)


async def create_bulk_users(users, session):

    for _ in range(users):

        args = {}
        args['email'] = "{}@{}".format(random_string(), random_string())
        args['username'] = random_string()
        args['hashed_pass'] = await get_password_hash(random_string())
        password = random_string()

        await User.AddNew(session, args)

    return True
