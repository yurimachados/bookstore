FROM python:3.10.12-slim as python-base

# Python:
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry:
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME='/opt/poetry' \
    # make poetry create virtualenvs in this location
    # Iit gets named .venv
    POETRY_VIRTUALENVS_IN_PROJECT=true\
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # path:
    # this is where our requirements + virtualenvs will live
    PYSETUP_PATH='/opt/pysetup' \
    VENV_PATH='/opt/pysetup/.venv'

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment.
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# install pestgres dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# copy in our build poetry + venv
#COPY --from=builder-base $POETRY_HOME $POETRY_HOME
#COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

WORKDIR /app

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]