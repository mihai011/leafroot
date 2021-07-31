FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# update and upgrade
RUN apt -y update 
RUN apt -y upgrade

RUN mkdir /workspace
WORKDIR /workspace

COPY /app .

RUN pip install --upgrade pip -r requirements.txt