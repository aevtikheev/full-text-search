FROM python:3.9.2-slim-buster

EXPOSE 8000

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.1.4

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi