FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
# FROM ubuntu:18.04

# update and upgrade
RUN apt -y update 
RUN apt -y upgrade

RUN mkdir /workspace
WORKDIR /workspace

# COPY /app .
# COPY /.env .

# RUN pip install --upgrade pip -r requirements.txt
