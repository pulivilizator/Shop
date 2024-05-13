FROM python:3.12.3-slim-bookworm as poetry_venv

ENV POETRY_HOME="/opt/poetry/" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY project .
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-ansi


FROM python:3.12.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=poetry_venv /app/.venv ./.venv
COPY project .