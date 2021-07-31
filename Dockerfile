FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir /workspace
WORKDIR /workspace

COPY app.py app.py