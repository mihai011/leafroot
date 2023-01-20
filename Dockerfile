FROM python:3.10 AS base

# update and upgrade
# RUN apt -y update
# RUN apt -y upgrade

RUN mkdir /workspace
WORKDIR /workspace

COPY . .

RUN make install_rust
ENV PATH="/root/.cargo/bin:${PATH}"
RUN make venv_create

FROM base AS dev
CMD sleep infinity

FROM base AS prod
CMD make start_production
