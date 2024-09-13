FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /EventX_API

COPY pyproject.toml /EventX_API/

RUN pip install poetry

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root

COPY . /EventX_API/

ENV DJANGO_SETTINGS_MODULE=event_management.settings

EXPOSE 8000

CMD ["poetry", "run", "python", "event_management/manage.py", "runserver"]