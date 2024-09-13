FROM python:3.11-slim

WORKDIR /EventX_API

COPY . /EventX_API

RUN pip install poetry
RUN cp .env.example .env
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root


ENV DJANGO_SETTINGS_MODULE=event_management.settings
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["poetry", "run", "python", "event_management/manage.py", "runserver", "0.0.0.0:8000"]