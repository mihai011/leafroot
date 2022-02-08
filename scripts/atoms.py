"""
module that crates atoms.json file
"""

import json
import random
import string


def random_string():
    """
    generate random string
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )


atoms = []
for i in range(200000):

    args = {}
    args["x"] = random.random()
    args["y"] = random.random()
    args["z"] = random.random()
    atoms.append(args)

with open("atoms.json", "w+",encoding="utf-8") as f:

    f.write(json.dumps(atoms))
