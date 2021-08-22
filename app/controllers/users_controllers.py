import random
import string 


from models import User
from controllers import parse, create_response_ok


def random_string():

  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def create_users(request):

  params = parse(request)

  for _ in range(int(params['quantity'])):

      args = {}
      args['email'] = "{}@{}".format(random_string(), random_string())
      args['username'] = random_string()
      args['verified'] = True

      User.AddNew(args)

  return create_response_ok("Users created succesfully!")