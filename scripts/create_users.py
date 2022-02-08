"""
just a file for experiments
"""

import json
import random
import string


def random_string():
    """
    generates a random string
    """

    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )


users = []
for i in range(20000):

    args = {}
    args["email"] = "{}@{}{}".format(random_string(), random_string(), i)
    args["username"] = random_string()
    args["password"] = random_string()
    users.append(args)

with open("users.json", "w+", encoding="utf-8") as f:

    f.write(json.dumps(users))
