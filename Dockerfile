FROM python:slim as python-base

RUN apt-get update
RUN apt-get install -y curl
RUN mkdir /src
RUN curl -o /src/get-poetry.py -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py

FROM python:slim as runtime

WORKDIR /src
COPY --from=python-base /src/get-poetry.py /src/
RUN python /src/get-poetry.py
COPY poetry.lock pyproject.toml /src/
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false
RUN poetry install  --no-dev
RUN rm -f /src/get-poetry.py

WORKDIR /
RUN mkdir /app
COPY app app

CMD export $(grep -v '^#' app/environment.env | xargs) && PYTHONPATH=.:app python app/main.py