# Order Management Service - basic CRUD operations

## Software Installation
Install on the server following software:
```
Python 3
PostgreSQL 
Redis
```

## App Installation
Prepare local POSTGRES database
```bash
#
sudo -u postgres psql -c "CREATE DATABASE orders_db"
sudo -u postgres psql -c "CREATE USER db_user WITH PASSWORD 'db_pass'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE orders_db to db_user"

#install libraries
pip install -r constraints.txt

#run migrations
alembic upgrade head
```