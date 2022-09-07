FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# update and upgrade
RUN apt -y update
RUN apt -y upgrade


RUN mkdir /workspace
WORKDIR /workspace

COPY . .

RUN make install_rust
ENV PATH="/root/.cargo/bin:${PATH}"

RUN make venv_create
RUN make rust_workers
