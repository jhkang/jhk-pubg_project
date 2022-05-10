FROM python:3.9.12

WORKDIR /home

COPY .env requirements.txt .
RUN pip install -r requirements.txt

COPY pubg_api/ ./pubg_api/

RUN apt-get update && apt-get install -y vim \
  && rm -rf /var/lib/apt/lists/*

WORKDIR pubg_api