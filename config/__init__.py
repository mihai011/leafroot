import os
import sys

from dotenv import dotenv_values

if "ENV" not in os.environ:
    print("FATAL! Environment variable not set up! Helping values: 'prod' or 'dev'")
    sys.exit(1)

if os.environ['ENV'] not in ["dev", "prod"]:
    print("FATAL! Environment variable not set up correctly! Helping values: 'prod' or 'dev'")
    sys.exit(1)

config = {}
# check up if environment is production
if os.environ['ENV'] == "dev":
    if os.path.exists(".env"):
        config = dotenv_values(".env")
    else:
        print("FATAL! Environment file not present! Try a '.env' in the root of the project!")
        sys.exit(1)


# check up if environment is production
if os.environ['ENV'] == "prod":
    # retrieve secrets frome external api's here
    pass

# check up if environment is CIRCLE CI
if os.environ.get("CIRCLECI", None):
    # replace environment variables with OPENCI variables
    for key, value in config.items():
        if key.startswith("CI_"):
            config[key.replace("CI_", "")] = value

# check mandatory fields
mandatory_fields = ["POSTGRES_DB",
"POSTGRES_HOST",
"POSTGRES_USER",
"POSTGRES_PASSWORD",
"ACCESS_TOKEN_EXPIRE_MINUTES",
"SECRET_KEY",
"ALGORITHM"]

missing_fields = []

for mandatory_field in mandatory_fields:
    if mandatory_field not in config:
        missing_fields.append(mandatory_field)

if missing_fields:
    missing_fields = '\n'.join(missing_fields)
    print("FATAL! The following environment "\
        "variables are missing:\n{}".format(missing_fields))
    os._exit(1)
