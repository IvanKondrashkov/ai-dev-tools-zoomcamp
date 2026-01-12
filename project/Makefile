.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build test test-backend test-backend-unit test-backend-integration test-frontend clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install              - Install dependencies for both frontend and backend"
	@echo "  make install-backend      - Install backend dependencies only"
	@echo "  make install-frontend     - Install frontend dependencies only"
	@echo "  make dev                   - Run development servers (requires concurrently)"
	@echo "  make dev-backend          - Run backend development server only"
	@echo "  make dev-frontend         - Run frontend development server only"
	@echo "  make build                 - Build production versions"
	@echo "  make test                  - Run all tests (backend + frontend)"
	@echo "  make test-backend          - Run all backend tests"
	@echo "  make test-backend-unit     - Run backend unit tests only"
	@echo "  make test-backend-integration - Run backend integration tests only"
	@echo "  make test-frontend         - Run frontend tests"
	@echo "  make clean                 - Clean build artifacts"
	@echo "  make docker-up             - Start services with Docker Compose"
	@echo "  make docker-down           - Stop Docker Compose services"

install: install-backend install-frontend

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && npm install

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Note: Install concurrently globally with 'npm install -g concurrently' if not already installed"
	concurrently "cd backend && uv run uvicorn app.main:app --reload" "cd frontend && npm run dev"

dev-backend:
	@echo "Starting backend development server..."
	@echo "Backend: http://localhost:8000"
	cd backend && uv run uvicorn app.main:app --reload

dev-frontend:
	@echo "Starting frontend development server..."
	@echo "Frontend: http://localhost:5173"
	cd frontend && npm run dev

build:
	cd backend && uv sync
	cd frontend && npm run build

test:
	@echo "Running backend tests..."
	cd backend && uv sync --extra test && uv run pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm test -- --run

test-backend:
	cd backend && uv sync --extra test && uv run pytest tests/ -v

test-backend-unit:
	cd backend && uv sync --extra test && uv run pytest tests/unit -v

test-backend-integration:
	cd backend && uv sync --extra test && uv run pytest tests/integration -v

test-frontend:
	cd frontend && npm test -- --run

clean:
	@echo "Cleaning build artifacts..."
	@if [ -d "backend/__pycache__" ]; then rm -rf backend/__pycache__; fi
	@if [ -d "backend/.pytest_cache" ]; then rm -rf backend/.pytest_cache; fi
	@if [ -d "backend/htmlcov" ]; then rm -rf backend/htmlcov; fi
	@if [ -d "backend/app/__pycache__" ]; then rm -rf backend/app/__pycache__; fi
	@if [ -d "backend/app/routers/__pycache__" ]; then rm -rf backend/app/routers/__pycache__; fi
	@if [ -d "backend/tests/__pycache__" ]; then rm -rf backend/tests/__pycache__; fi
	@if [ -d "backend/tests/unit/__pycache__" ]; then rm -rf backend/tests/unit/__pycache__; fi
	@if [ -d "backend/tests/integration/__pycache__" ]; then rm -rf backend/tests/integration/__pycache__; fi
	@if [ -d "frontend/dist" ]; then rm -rf frontend/dist; fi
	@if [ -d "frontend/node_modules/.vite" ]; then rm -rf frontend/node_modules/.vite; fi
	@echo "Clean complete."

docker-up:
	cd infra && docker-compose up --build

docker-down:
	cd infra && docker-compose down

