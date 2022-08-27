FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# update and upgrade
RUN apt -y update
RUN apt -y upgrade
RUN apt install moreutils -y


RUN mkdir /workspace
WORKDIR /workspace

COPY . .

# RUN pip install --upgrade pip -r requirements.txt
