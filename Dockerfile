FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . .

ENV DJANGO_ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p 8000 config.asgi:application"]