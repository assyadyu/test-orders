#!/bin/bash

python -m pytest tests/ -s -vv -W ignore::DeprecationWarning

# Run migrations
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
