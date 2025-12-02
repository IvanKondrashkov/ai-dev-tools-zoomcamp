# Docker Infrastructure

This directory contains Docker configuration files for containerizing the Coding Interview Platform.

## Files

- `docker-compose.yml` - Docker Compose configuration with PostgreSQL, Backend, and Frontend services
- `../backend/Dockerfile` - Dockerfile for the FastAPI backend service
- `../frontend/Dockerfile` - Dockerfile for the React frontend service

## Prerequisites

- Docker Desktop or Docker Engine installed
- Docker Compose v2.0+

## Quick Start

### Build and start all services

```bash
cd infra
docker-compose up --build
```

### Start services in detached mode

```bash
docker-compose up -d
```

### Stop all services

```bash
docker-compose down
```

### Stop and remove volumes (including database data)

```bash
docker-compose down -v
```

## Services

### PostgreSQL

- **Port:** 5432
- **Database:** coding_interview_db
- **User:** coding_interview
- **Password:** coding_interview_password
- **Volume:** postgres_data (persistent storage)

### Backend (FastAPI)

- **Port:** 8000
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Includes:** Go and Java compilers for code execution

### Frontend (React + Vite)

- **Port:** 3000
- **URL:** http://localhost:3000
- **Environment:** VITE_API_URL (defaults to http://backend:8000 in Docker)

## Environment Variables

### Backend

- `DATABASE_URL` - PostgreSQL connection string
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)
- `POSTGRES_HOST` - PostgreSQL hostname
- `POSTGRES_PORT` - PostgreSQL port
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `POSTGRES_DB` - PostgreSQL database name

### Frontend

- `VITE_API_URL` - Backend API URL (defaults to http://backend:8000 in Docker)

## Development

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Execute commands in containers

```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh

# PostgreSQL
docker-compose exec postgres psql -U coding_interview -d coding_interview_db
```

### Rebuild specific service

```bash
docker-compose build backend
docker-compose up -d backend
```

## Production Considerations

For production deployment, consider:

1. **Security:**
   - Change default database passwords
   - Use secrets management (Docker secrets, environment files)
   - Enable SSL/TLS for database connections
   - Implement proper CORS policies

2. **Performance:**
   - Use production builds (not development mode)
   - Configure resource limits (CPU, memory)
   - Use reverse proxy (nginx, traefik)
   - Enable database connection pooling

3. **Monitoring:**
   - Add health checks
   - Set up logging aggregation
   - Monitor resource usage
   - Set up alerts

4. **Database:**
   - Use managed database service (RDS, Cloud SQL)
   - Set up regular backups
   - Configure replication for high availability

## Troubleshooting

### Port already in use

If ports 3000, 8000, or 5432 are already in use, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Use 3001 instead of 3000
```

### Database connection issues

Check if PostgreSQL is healthy:

```bash
docker-compose ps
docker-compose logs postgres
```

### Frontend can't connect to backend

Verify the `VITE_API_URL` environment variable is set correctly. In Docker, it should be `http://backend:8000` (using service name).

### Code execution not working

Ensure Go and Java are installed in the backend container:

```bash
docker-compose exec backend go version
docker-compose exec backend java -version
```

