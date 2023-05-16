ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION AS base


RUN mkdir /leafroot
WORKDIR /leafroot

COPY . .
RUN pip install poetry
RUN make venv_create

FROM base AS dev
RUN bash scripts/install_sonar.sh
CMD sleep infinity

FROM base AS prod
CMD make start_production_docker

FROM base as worker
CMD make start_celery_workers
