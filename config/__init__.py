import os
import sys

from dotenv import dotenv_values

if "ENV_FILE" not in os.environ:
    print(
        "FATAL! Environment ENV_FILE variable not set up! Path of a env fiel needed."
    )
    sys.exit(1)

env_path = os.environ["ENV_FILE"]
config = {}
if os.path.exists(env_path):
    config = dotenv_values(env_path)
else:
    print(
        "FATAL! Environment file not present! Try a '.env' in the root of the project!"
    )
    sys.exit(1)

if config["ENV"] not in ["dev", "prod"]:
    print(
        "FATAL! Environment variable not set up correctly! Helping values: 'prod' or 'dev'"
    )
    sys.exit(1)

# check up if environment is production
if config["ENV"] == "prod":
    # retrieve secrets frome external api's here
    pass

mandatory_fields = [
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "SECRET_KEY",
    "ALGORITHM",
    "REDIS_HOST",
    "RABBITMQ_HOST",
    "INTERFACE",
]


# check up if environment dictates something else
# with the values for the environment
for key, value in os.environ.items():
    if key in mandatory_fields:
        config[key] = value

# only if interface is set we overwrite the external services
if config["INTERFACE"]:
    config["REDIS_HOST"] = config["INTERFACE"]
    config["RABBITMQ_HOST"] = config["INTERFACE"]
    config["POSTGRES_HOST"] = config["INTERFACE"]


# check mandatory fields
missing_fields = []

for mandatory_field in mandatory_fields:
    if mandatory_field not in config:
        missing_fields.append(mandatory_field)

if missing_fields:
    missing_fields = "\n".join(missing_fields)
    print(
        "FATAL! The following environment "
        "variables are missing:\n{}".format(missing_fields)
    )
    os._exit(1)

CELERY_BROKER_URL = "amqp://{}:5672".format(config["RABBITMQ_HOST"])
CELERY_RESULT_BACKEND = "redis://{}:6379".format(config["REDIS_HOST"])
