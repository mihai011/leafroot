#!/usr/bin/env bash

set -euo pipefail

LD_PRELOAD="/usr/lib/$(uname -m)-linux-gnu/libstdc++.so.6"
export LD_PRELOAD

unset PIP_USER
umask 0002


echo "Container's IP address: `awk 'END{print $1}' /etc/hosts`"
echo  "Executed command: $1"

if [ "$1" = 'standalone' ]; then
    poetry run airflow standalone
fi

if [ "$1" = 'init' ]; then
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
