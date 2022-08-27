from celery import Celery
from config import config

CELERY_BROKER_URL = "amqp://{}:5672".format(config["RABBITMQ_HOST"])
CELERY_RESULT_BACKEND = "redis://{}:6379".format(config["REDIS_HOST"])

app = Celery(__name__, backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)


@app.task
def small_task(name="small_task"):
    print("Small Task")
    return {"small_task": 1}
