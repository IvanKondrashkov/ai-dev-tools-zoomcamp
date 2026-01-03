.PHONY: help install test run migrate shell clean docker-up docker-down docker-logs docker-test

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

test: ## Run tests
	uv run python manage.py test

test-verbose: ## Run tests with verbose output
	uv run python manage.py test --verbosity=2

run: ## Run development server
	uv run python manage.py runserver

migrate: ## Run database migrations
	uv run python manage.py migrate

makemigrations: ## Create new migrations
	uv run python manage.py makemigrations

shell: ## Open Django shell
	uv run python manage.py shell

createsuperuser: ## Create Django superuser
	uv run python manage.py createsuperuser

collectstatic: ## Collect static files
	uv run python manage.py collectstatic --noinput

clean: ## Clean Python cache files
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true

# Docker commands
docker-up: ## Start Docker containers
	cd infra && docker-compose up -d

docker-down: ## Stop Docker containers
	cd infra && docker-compose down

docker-logs: ## View Docker logs
	cd infra && docker-compose logs -f

docker-test: ## Run tests in Docker container
	cd infra && docker-compose exec todo-app python manage.py test

docker-shell: ## Open shell in Docker container
	cd infra && docker-compose exec todo-app python manage.py shell

docker-migrate: ## Run migrations in Docker container
	cd infra && docker-compose exec todo-app python manage.py migrate

docker-createsuperuser: ## Create superuser in Docker container
	cd infra && docker-compose exec todo-app python manage.py createsuperuser

docker-restart: ## Restart Docker containers
	cd infra && docker-compose restart

docker-rebuild: ## Rebuild and restart Docker containers
	cd infra && docker-compose up -d --build

docker-clean: ## Stop and remove Docker containers and volumes
	cd infra && docker-compose down -v


