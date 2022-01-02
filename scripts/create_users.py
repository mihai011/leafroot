import json
import random
import string 

def random_string():

  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

users = []
for i in range(20000):

    args = {}
    args['email'] = "{}@{}{}".format(random_string(), random_string(), i)
    args['username'] = random_string()
    args['password'] = random_string()
    users.append(args)

with open("users.json", "w+") as f:

  f.write(json.dumps(users))