FROM python:3.8-slim

RUN mkdir /app
RUN mkdir /aszulc-input
RUN mkdir /aszulc-output

COPY app app
COPY input-data aszulc-input

WORKDIR /

RUN pip install -r app/requirements.txt

CMD PYTHONPATH=.:app python app/main.py