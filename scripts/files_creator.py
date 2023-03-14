# pylint: disable-all
"""Module that creates different files for manual testing."""

import json
import random
import string


def random_string():
    """Generate random string."""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )


atoms = []
for i in range(200000):
    args = {}
    args["x"] = random.random()
    args["y"] = random.random()
    args["z"] = random.random()
    atoms.append(args)

with open("atoms.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(atoms))


users = []
for i in range(20000):
    args = {}
    args["email"] = "{}@{}{}".format(random_string(), random_string(), str(i))
    args["username"] = random_string()
    args["password"] = random_string()
    users.append(args)

with open("users.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(users))
