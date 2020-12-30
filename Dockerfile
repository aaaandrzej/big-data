FROM python:3.8-slim

RUN mkdir /app

COPY app app

WORKDIR /

RUN pip install -r app/requirements.txt

CMD export $(grep -v '^#' app/environment.env | xargs) && PYTHONPATH=.:app python app/main.py