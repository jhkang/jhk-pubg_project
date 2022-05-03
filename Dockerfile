FROM python:3.9.12

WORKDIR "/home"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pubg_api/ /pubg_api/