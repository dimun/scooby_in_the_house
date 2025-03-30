# Docker Setup for Scooby In The House

This project includes Docker configuration for easy development and deployment. You can run different components independently or all together.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuration

The default configuration values are stored in the `.env` file. You can modify this file to change database credentials, ports, etc.

## Docker Compose Files

There are multiple Docker Compose files for different use cases:

1. `docker-compose.yml` - Only PostgreSQL database
2. `backend/docker-compose.yml` - Backend service with PostgreSQL
3. `docker-compose.full.yml` - All services (PostgreSQL, Backend, Frontend)

## Running the Database Only

To start the PostgreSQL database:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432

## Running the Backend with Database

To start the backend service with PostgreSQL:

```bash
cd backend
docker-compose up -d
```

## Running All Services

To start all services (database, backend, and frontend):

```bash
docker-compose -f docker-compose.full.yml up -d
```

This will start:
- PostgreSQL on port 5432
- Backend API on port 8000 (access at http://localhost:8000)
- Frontend on port 5173 (access at http://localhost:5173)

## Stopping Services

To stop and remove the containers:

```bash
docker-compose down  # For database only
# or
docker-compose -f docker-compose.full.yml down  # For all services
```

To stop and remove containers including volumes (database data):

```bash
docker-compose down -v  # For database only
# or
docker-compose -f docker-compose.full.yml down -v  # For all services
```

## Connecting to PostgreSQL

To connect to the database directly:

```bash
docker exec -it scooby_db psql -U postgres -d scooby_db
```

Or use any PostgreSQL client with these credentials:
- Host: localhost
- Port: 5432
- Database: scooby_db
- Username: postgres
- Password: postgres

## Troubleshooting

If you encounter issues:

1. Check docker logs:
   ```bash
   docker-compose logs  # For database only
   # or
   docker-compose -f docker-compose.full.yml logs  # For all services
   ```

2. Check specific service logs:
   ```bash
   docker-compose logs db
   docker-compose logs backend
   docker-compose -f docker-compose.full.yml logs frontend
   ```

3. Restart a specific service:
   ```bash
   docker-compose restart db
   docker-compose -f docker-compose.full.yml restart backend
   ```

## Development Workflow

When developing:

1. The backend code is mounted as a volume, so changes will be detected and the server will reload automatically.
2. The frontend code is also mounted as a volume, so changes will be detected and hot-reloaded.
3. To run migrations after schema changes, you can run:
   ```bash
   docker-compose -f docker-compose.full.yml exec backend alembic upgrade head
   ``` 