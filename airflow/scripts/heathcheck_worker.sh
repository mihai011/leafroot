celery --app airflow.executors.celery_executor.app inspect ping -d "celery@${HOSTNAME}"
