# Coding Interview Platform

A real-time collaborative coding interview platform built with React + Vite (frontend) and Python + FastAPI (backend).

## Features

- ✅ Create shareable coding session links
- ✅ Real-time collaborative code editing
- ✅ Syntax highlighting for JavaScript, Python, Go, and Java
- ✅ Code execution:
  - **JavaScript**: Direct execution in browser
  - **Python**: Pyodide (Python in WebAssembly) - executes in browser
  - **Go**: Server-side execution (requires Go installed on server)
  - **Java**: Server-side execution (requires JDK installed on server)
- ✅ WebSocket-based real-time updates

## Prerequisites

### For Local Development

- Node.js 18+ and npm
- Python 3.11+
- `uv` package manager (install with `pip install uv`)
- **Go 1.20+** (for Go code execution) - [Install Go](https://go.dev/doc/install)
- **Java JDK 11+** (for Java code execution) - [Install JDK](https://www.oracle.com/java/technologies/downloads/)

**Note:** Go and Java are only required if you want to execute Go/Java code on the server. JavaScript and Python execute in the browser.

### For Docker Deployment

- Docker Desktop or Docker Engine
- Docker Compose v2.0+

**Note:** Docker setup includes PostgreSQL, Go, and Java automatically.

## Installation

### Option 1: Docker (Recommended)

The easiest way to run the application is using Docker Compose:

```bash
cd infra
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend on port 3000

See [infra/README.md](infra/README.md) for detailed Docker documentation.

### Option 2: Local Development

#### Install all dependencies

```bash
make install
```

Or install separately:

```bash
# Frontend
make install-frontend

# Backend
make install-backend
```

## Running the Application

### Using Docker

```bash
cd infra
docker-compose up
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Local Development

#### Run both frontend and backend concurrently

```bash
make dev
```

Or run separately in different terminals:

```bash
# Terminal 1 - Frontend
make run-frontend

# Terminal 2 - Backend
make run-backend
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing

### Run all tests

```bash
make test
```

### Run tests separately

```bash
# Frontend tests
make test-frontend

# Backend tests
make test-backend
```

### Backend Test Structure

Backend tests are organized into two categories:

**Unit Tests** (`backend/tests/unit/`):
- Fast, isolated tests that mock dependencies
- Test individual functions and components
- No database or external services required

```bash
# Run only unit tests
cd backend && uv run pytest tests/unit/ -v
```

**Integration Tests** (`backend/tests/integration/`):
- Test full API endpoints and WebSocket functionality
- Require database and/or running server
- Test interactions between components

```bash
# Run only integration tests
cd backend && uv run pytest tests/integration/ -v

# Note: Integration tests require the backend server to be running
# Terminal 1 - Start the backend server
make run-backend

# Terminal 2 - Run integration tests
cd backend && uv run pytest tests/integration/ -v
```

### Frontend Test Structure

Frontend tests are located in component directories:
- `src/components/__tests__/` - Component tests
- `src/utils/__tests__/` - Utility function tests
- `src/App.test.jsx` - App component tests

```bash
# Run frontend tests
cd frontend && npm test
```

## Project Structure

```
homework2/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── database.py    # Database models and connection
│   ├── db_service.py  # Database service functions
│   ├── migrations.py  # Database migration script
│   ├── tests/
│   ├── pyproject.toml
│   └── pytest.ini
├── infra/             # Docker infrastructure
│   ├── docker-compose.yml
│   └── init-db/       # Database initialization scripts
├── backend/
│   └── Dockerfile     # Backend Dockerfile
└── frontend/
    └── Dockerfile     # Frontend Dockerfile
│       ├── 01-init.sql
│       ├── 02-seed.sql
│       └── 03-run-migrations.sh
├── openapi.yaml       # OpenAPI specification
├── Makefile          # Build automation
└── README.md
```

## API Endpoints

- `POST /api/sessions` - Create a new coding session
- `GET /api/sessions/{session_id}` - Get session information
- `POST /api/execute` - Execute code (client-side for JS/Python, server-side for Go/Java)

## Database

The application uses PostgreSQL to persist session data.

### Data Stored in Database

**`sessions` table:**
- `session_id` - Unique identifier for each coding session
- `code` - Current code content in the editor
- `language` - Selected programming language (javascript, python, go, java)
- `created_at` - Timestamp when session was created
- `updated_at` - Timestamp of last update (auto-updated)

**`code_history` table (optional):**
- `id` - Auto-incrementing ID
- `session_id` - Reference to session
- `code` - Code snapshot
- `language` - Language at time of change
- `changed_at` - Timestamp of change

### Database Initialization

When using Docker, the database is automatically initialized with:
1. SQL scripts from `infra/init-db/` (run on first container creation)
2. Python migrations from `backend/migrations.py` (run on backend startup)

See [infra/init-db/README.md](infra/init-db/README.md) for details.

## WebSocket Events

- `join_session` - Join a coding session
- `code_change` - Broadcast code changes
- `language_change` - Broadcast language changes
- `code_update` - Receive code updates
- `language_update` - Receive language updates

## Development

### Backend Development

The backend uses `uv` for dependency management:

```bash
# Add a new package
cd backend
uv add <PACKAGE-NAME>

# Sync dependencies
uv sync

# Run with uvicorn
uv run uvicorn main:socket_app --reload
```

### Server-Side Code Execution Setup

For Go and Java code execution, you need to install the respective compilers:

**Go:**
```bash
# Check if Go is installed
go version

# If not installed, download from https://go.dev/doc/install
```

**Java:**
```bash
# Check if Java is installed
java -version
javac -version

# If not installed, download JDK from https://www.oracle.com/java/technologies/downloads/
```

**Security Note:** The current implementation executes code in temporary directories with timeouts (10 seconds). For production use, consider:
- Using Docker containers for better isolation
- Implementing resource limits (CPU, memory)
- Adding sandboxing mechanisms
- Implementing rate limiting

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Makefile Commands

Run `make help` to see all available commands:

- `make install` - Install all dependencies
- `make test` - Run all tests
- `make run` - Run frontend and backend (separate terminals)
- `make dev` - Run both concurrently
- `make clean` - Clean build artifacts

## License

This project is part of the AI Dev Tools Zoomcamp course.

