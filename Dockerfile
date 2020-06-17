FROM python:3.7-slim as build

RUN mkdir -p /app/fut_market_prediction/

COPY . /app/fut_market_prediction/

WORKDIR /app/

COPY requirements.txt /tmp

WORKDIR /tmp

ENV DB_USERNAME='postgres'
ENV DB_PASSWORD='postgres1'
ENV DB_HOST='localhost'
ENV DB_PORT='5432'
ENV DB_DB_NAME='fut_market_prediction'

RUN pip install -r requirements.txt

WORKDIR /app/fut_market_prediction/

EXPOSE 8080