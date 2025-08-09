ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION AS base

RUN mkdir /leafroot
WORKDIR /leafroot

COPY . .
RUN apt update && apt-get install -y python3-dev
RUN make venv_create
RUN apt update && apt install -y iputils-ping

FROM base AS dev
CMD sleep infinity

FROM base AS prod
CMD make start_production_docker

FROM base as worker
CMD make start_celery_workers
