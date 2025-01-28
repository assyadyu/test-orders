# Order Management Service - basic CRUD operations

## Software Installation
Option 1. Manual Setup 

Install on the server following software:
```
Python 3
PostgreSQL 
Redis
RabbitMQ
```

## App Installation
Prepare local POSTGRES database orders_db and order_db_test for running tests with pytest
```bash
#
sudo -u postgres psql -c "CREATE DATABASE orders_db"
sudo -u postgres psql -c "CREATE USER db_user WITH PASSWORD 'db_pass'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE orders_db to db_user"
```
Set environment variables (see app/common/settings.py)

and run
```bash
# install libraries
pip install -r constraints.txt

# run migrations
alembic upgrade head

# run server -- make sure auth server is running
uvicorn app.main:app --reload

# Swagger UI
http://127.0.0.1:8000/docs#/

# run tests
pytest 

# check test coverage
pytest --cov
```

Option 2. Using Docker

Note: Build container from test-auth repo after building this one
```bash
docker compose up --build
# run with testing profile that executes tests
docker compose --profile testing up --build

# Swagger UI
http://0.0.0.0/docs#/
```