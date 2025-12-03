.PHONY: help install install-frontend install-backend test test-frontend test-backend test-backend-unit test-backend-integration run run-frontend run-backend dev clean docker-up docker-down docker-build docker-logs docker-restart docker-clean docker-reset-db

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation commands
install: install-frontend install-backend ## Install all dependencies

install-frontend: ## Install frontend dependencies
	cd frontend && npm install

install-backend: ## Install backend dependencies
	cd backend && uv sync

# Test commands
test: test-frontend test-backend ## Run all tests

test-frontend: ## Run frontend tests
	cd frontend && npm test -- --run

test-backend: ## Run backend tests (unit tests only, integration tests require DB)
	cd backend && uv run pytest -m "not integration"

test-backend-unit: ## Run backend unit tests only
	cd backend && uv run pytest tests/unit/ -v

test-backend-integration: ## Run backend integration tests only
	cd backend && uv run pytest tests/integration/ -v

# Development commands
run: run-frontend run-backend ## Run both frontend and backend (in separate terminals)

run-frontend: ## Run frontend development server
	cd frontend && npm run dev

run-backend: ## Run backend development server
	cd backend && uv run uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000

dev: ## Run both frontend and backend concurrently
	cd frontend && npm install concurrently --save-dev && npm run dev:all

# Cleanup commands
clean: ## Clean build artifacts and dependencies
	cd frontend && rm -rf node_modules dist
	cd backend && rm -rf .venv .uv __pycache__ .pytest_cache

# Docker commands
docker-up: ## Start Docker containers
	cd infra && docker-compose up -d

docker-down: ## Stop Docker containers
	cd infra && docker-compose down

docker-build: ## Build Docker containers
	cd infra && docker-compose build

docker-logs: ## Show Docker containers logs
	cd infra && docker-compose logs -f

docker-restart: ## Restart Docker containers
	cd infra && docker-compose restart

docker-clean: ## Stop and remove Docker containers, volumes, and networks
	cd infra && docker-compose down -v --remove-orphans

docker-reset-db: ## Reset PostgreSQL database (removes volume and recreates)
	cd infra && docker-compose stop postgres
	cd infra && docker-compose rm -f postgres
	-docker volume rm infra_coding_interview_postgres_data
	cd infra && docker-compose up -d postgres

