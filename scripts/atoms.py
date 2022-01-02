import json
import random
import string 

def random_string():

  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

atoms = []
for i in range(200000):

    args = {}
    args['x'] = random.random()
    args['y'] = random.random()
    args['z'] = random.random()
    atoms.append(args)

with open("atoms.json", "w+") as f:

  f.write(json.dumps(atoms))