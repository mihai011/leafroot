import random, string

from fastapi.responses import JSONResponse


from models import User


def random_string():

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def parse(request):

  args = request.path_params

  return args

def create_response_ok(message):

  data = {}  
  data['message'] = message
  data['status'] = 200
  return JSONResponse(content=data)

def create_response_bad(message):

  data = {}  
  data['message'] = message
  data['status'] = 400
  return JSONResponse(content=data)


async def create_bulk_users(users):

  for _ in range(users):

    args = {}
    args['email'] = "{}@{}".format(random_string(), random_string())
    args['username'] = random_string()
    args['verified'] = True

    User.AddNew(args)

  return True

