import random, string, json

from fastapi.responses import ORJSONResponse

from data import User, Token


def random_string():

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def parse(request):

  if request.method == "GET":
    args = request.path_params

  if request.method == "POST":
    args = request.json()

  return args

def create_response_ok(message, item=None):

  data = {}  
  data['message'] = message
  data['item'] = item
  data['status'] = 200
  return ORJSONResponse(content=data)

def create_response_bad(message, item=None):

  data = {}  
  data['message'] = message
  data['item'] = item
  data['status'] = 400
  return ORJSONResponse(content=data)


async def create_bulk_users(users, session):

  for _ in range(users):

    args = {}
    args['email'] = "{}@{}".format(random_string(), random_string())
    args['username'] = random_string()
    password = random_string()

    await User.AddNew(session, args)

    token_args = {}
    token_args['password'] = password
    token_args['email'] = args['email']

    await Token.AddNew(session, token_args)
    
  return True

