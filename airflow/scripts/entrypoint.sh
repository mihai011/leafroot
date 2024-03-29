#!/bin/bash

set -euo pipefail

LD_PRELOAD="/usr/lib/$(uname -m)-linux-gnu/libstdc++.so.6"
export LD_PRELOAD

unset PIP_USER
umask 0002

CREATE_PAYLOAD="CREATE DATABASE ${AIRFLOW_DB};CREATE USER ${AIRFLOW_DB_USER}
                WITH SUPERUSER ENCRYPTED PASSWORD '${AIRFLOW_DB_PASS}';
                GRANT ALL ON SCHEMA public TO ${AIRFLOW_DB_USER};
                GRANT ALL PRIVILEGES ON DATABASE ${AIRFLOW_DB} TO ${AIRFLOW_DB_USER};"





AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${AIRFLOW_DB_USER}:${AIRFLOW_DB_PASS}@${AIRFLOW_DB_HOST}/${AIRFLOW_DB}"
AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://${AIRFLOW_DB_USER}:${AIRFLOW_DB_PASS}@${AIRFLOW_DB_HOST}/${AIRFLOW_DB}"
AIRFLOW__CELERY__BROKER_URL="${REDIS_PROTOCOL}://:@${REDIS_HOST}:6379/0"

AIRFLOW_DB_UPGRADE=true
_AIRFLOW_WWW_USER_CREATE=true
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
_PIP_ADDITIONAL_REQUIREMENTS=''

CONNECTION_CHECK_MAX_COUNT='0'
# Required to handle warm shutdown of the celery workers properly
# See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
DUMB_INIT_SETSID='0'

export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN \
    AIRFLOW__CELERY__RESULT_BACKEN \
    AIRFLOW__CELERY__BROKER_URL \
    AIRFLOW_DB_UPGRADE \
    _AIRFLOW_WWW_USER_CREATE \
    _AIRFLOW_WWW_USER_CREATE \
    _AIRFLOW_WWW_USER_PASSWORD \
    _PIP_ADDITIONAL_REQUIREMENTS \
    CONNECTION_CHECK_MAX_COUNT \
    DUMB_INIT_SETSID




echo $AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
echo $AIRFLOW__CELERY__RESULT_BACKEND
echo $AIRFLOW__CELERY__BROKER_URL


echo "Container's IP address: `awk 'END{print $1}' /etc/hosts`"
echo  "Executed command: $1"

if [ "$1" = 'export' ]; then
    return 0
fi

if [ "$1" = 'standalone' ]; then
    poetry run airflow standalone
fi

if [ "$1" = 'init' ]; then
    echo $CREATE_PAYLOAD | PGPASSWORD=$POSTGRES_PASSWORD psql --user $POSTGRES_USER --host $POSTGRES_HOST
    poetry run airflow db check
    poetry run airflow db init
    poetry run airflow users create \
          --username $AIRFLOW_DEFAULT_USER \
          --firstname FIRST_NAME \
          --lastname LAST_NAME \
          --role Admin \
          --email admin@example.org \
          --password $AIRFLOW_DEFAULT_PASS
    exit 0
fi

if [ "$1" = 'webserver' ]; then
    poetry run airflow webserver
fi

if [ "$1" = 'scheduler' ]; then
    poetry run airflow scheduler
fi

if [ "$1" = 'triggerer' ]; then
    poetry run airflow triggerer
fi

if [ "$1" = 'worker' ]; then
    poetry run airflow celery worker
fi

if [ "$1" = 'flower' ]; then
    poetry run airflow celery flower
fi

exec "$@"
