# Event Management API

This project provides a Django-based REST API for managing events with JWT authentication, event registration, Celery background email notifications, Docker setup, and API documentation via drf-spectacular.

## Clone the Repository

```
git clone https://github.com/PavelSemenikhin/Event-Management-Test-Task.git
cd event-management-test-task
```

### Install Poetry


```
pip install poetry
poetry install
```

## Copy Environment Variables

A template `.env.sample` is included.  
Create the actual `.env` file:

```
cp .env.sample .env
```

Then update the required variables inside `.env`.

## Run the Project with Docker

Build and start all services:

```
docker compose up --build
```

This will start:
- Django app
- PostgreSQL database
- Redis
- Celery worker

After startup the API is available at:

```
http://localhost:8001/api/
```

Swagger documentation:

```
http://localhost:8001/api/docs/
```

## Running Black and Flake8 Inside Docker

### Run Black formatter

```
docker exec -it event-management-test-task-app-1 black .
```

### Run Flake8 linter

```
docker exec -it event-management-test-task-app-1 flake8 .
```


## Create Superuser

```
docker exec -it event-management-test-task-app-1 python manage.py createsuperuser
```

## Celery Worker

Celery starts automatically via docker compose and handles email notifications on event registration.
