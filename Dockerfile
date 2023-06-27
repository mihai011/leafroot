ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION AS base

RUN mkdir /leafroot
WORKDIR /leafroot

COPY . .
RUN pip install poetry
RUN make venv_create
RUN apt update && apt install -y iputils-ping

FROM base AS dev
CMD sleep infinity

FROM base AS prod
CMD make start_production_docker

FROM base as worker
CMD make start_celery_workers
