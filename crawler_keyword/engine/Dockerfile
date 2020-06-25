FROM python:3

WORKDIR /app


COPY ./requirements.txt /app/requirements.txt

RUN apt-get update
RUN pip install -r requirements.txt

COPY . .


