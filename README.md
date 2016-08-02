# Data tracking example with Falcon Web Framework

This simple RESTful API is created for high-performance handling of e-commerce data. It is build upon Falcon, PostgreSQL, SQLAlchemy, Redis, Celery, ujson, uWSGI, pytest, coverage, mock etc. in Python Programming Language ecosystem.

Application achieve 100% test coverage score.

## Usage

At first, install necessary requirements:
> pip install -r requirements.txt

Then, you need to have following services running by:

Postgres:
> sudo service postgresql start

Redis:
> redis-server

Celery:
> celery -A tracker.tasks:app worker --loglevel=info

uWSGI:
> uwsgi --http 127.0.0.1:8000 --wsgi-file tracker/urls.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191

## Tests

To run tests:
> py.test

For test coverage:
> py.test --cov tracker