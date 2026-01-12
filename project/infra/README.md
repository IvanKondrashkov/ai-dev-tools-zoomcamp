# Infrastructure

This directory contains infrastructure configuration and setup scripts.

## Structure

- `docker-compose.yml` - Docker Compose configuration for all services
- `init-db/` - PostgreSQL database initialization scripts

## Usage

### Start all services

```bash
cd infra
docker-compose up --build
```

### Stop all services

```bash
cd infra
docker-compose down
```

### View logs

```bash
cd infra
docker-compose logs -f
```

### Database Initialization

SQL scripts in `init-db/` are automatically executed when the PostgreSQL container starts for the first time. They run in alphabetical order.

To add new initialization scripts:
1. Create a new SQL file with a numeric prefix (e.g., `02-seed-data.sql`)
2. Scripts are executed in alphabetical order
3. Make scripts idempotent (safe to run multiple times)

## Services

- **db** - PostgreSQL 15 database
- **backend** - FastAPI backend service
- **frontend** - React frontend service (Nginx)

## Volumes

- `postgres_data` - Persistent PostgreSQL data storage
- `../backend/uploads` - Resume file uploads directory

