FROM python:3.12-slim AS base

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV ROOT=/app
ENV PYTHONPATH="3.12:/app/src/"

WORKDIR $ROOT

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && apt-get install -y --no-install-recommends apt-utils \
  && apt-get install -y --no-install-recommends libc-dev \
  && apt-get install -y --no-install-recommends gcc \
  && apt-get install -y --no-install-recommends gettext \
  && apt-get install -y --no-install-recommends screen \
  && apt-get install -y --no-install-recommends vim \
  && apt-get clean

ENV VIRTUALENV=$ROOT/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH=$VIRTUALENV/bin:$PATH

COPY constraints.txt pytest.ini ./
COPY src/tests/ $ROOT/tests/
COPY src/app/ $ROOT/app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r constraints.txt

FROM python:3.12-slim
ENV ROOT=/app
COPY --from=base $ROOT/venv $ROOT/venv
ENV PATH="$ROOT/venv/bin:$PATH"

COPY commands/ $ROOT/commands/
RUN chmod +x $ROOT/commands/*
ENV PATH="$ROOT/commands:$PATH"

ADD src $ROOT/src

WORKDIR $ROOT/src

CMD ["alembic", "upgrade", "head", ";","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
