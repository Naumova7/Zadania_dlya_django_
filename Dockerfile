FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["daphne", "config.asgi:application", "-p", "8000"]