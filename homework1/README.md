# Django TODO Application

A simple TODO application built with Django that allows you to create, edit, delete TODOs, assign due dates, and mark them as resolved.

## Features

- ✅ Create, edit and delete TODOs
- 📅 Assign due dates to TODOs
- ✓ Mark TODOs as resolved
- 🎨 Minimalist UI
- 🧪 Comprehensive test coverage
- 🐳 Docker support with PostgreSQL
- 📊 SQL-based database migrations for Docker deployments

## Requirements

- Python 3.11 or higher
- Django 5.0+
- PostgreSQL (or use Docker Compose)
- Docker and Docker Compose (for containerized deployment)
- `uv` for dependency management (recommended) or `pip`
- `make` for convenience commands (optional)

## Quick Start (Local Testing)

To quickly test the application locally:

```bash
# 1. Navigate to project directory
cd homework1

# 2. Install dependencies (creates .venv in homework1/)
uv sync

# 3. Run migrations (uses SQLite for local dev)
uv run python manage.py migrate

# 4. (Optional) Run tests to verify everything works
make test

# 5. Start the server
uv run python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

**Note**: 
- For local testing, you don't need PostgreSQL - Django will use SQLite automatically
- Tests also use SQLite in-memory database, so no database setup is required
- `uv sync` creates a `.venv` folder in `homework1/` directory (this is correct)
- If you have old `venv/` folders, you can safely delete them
- For production-like setup with PostgreSQL, use Docker (see Option 2 below)

## Installation

### Option 1: Local Development (without Docker)

1. **Navigate to project directory**:

```bash
cd homework1
```

2. **Install dependencies using uv**:

```bash
uv sync
```

This will:
- Install all dependencies from `pyproject.toml`
- Create a `.venv` folder in `homework1/` directory (this is correct and expected)
- Install the project in editable mode (allows Django to find the project modules)

3. **Set up environment variables** (optional, for PostgreSQL):

If you're using PostgreSQL locally, copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

Edit `.env` with your database settings. If you don't set up `.env`, the application will use default values from `settings.py`.

**Note**: For local testing without PostgreSQL, Django will use SQLite in-memory database for tests automatically.

4. **Run migrations** to create the database:

```bash
make migrate
```

Or manually:
```bash
uv run python manage.py migrate
```

5. **Create a superuser** (optional, for admin access):

```bash
make createsuperuser
```

Or manually:
```bash
uv run python manage.py createsuperuser
```

6. **Start the development server**:

```bash
make run
```

Or manually:
```bash
uv run python manage.py runserver
```

7. **Verify the application is running**:

Open your browser and navigate to `http://127.0.0.1:8000/`

You should see the TODO application homepage. You can:
- Create new TODOs by clicking "+ New"
- Edit existing TODOs
- Mark TODOs as resolved
- Delete TODOs

To access the admin panel, go to `http://127.0.0.1:8000/admin/` (requires superuser account).

### Option 2: Docker Compose (Recommended)

1. **Start services**:

```bash
make docker-up
```

Or manually:
```bash
cd infra && docker-compose up -d
```

This will:
- Start PostgreSQL database container
- Build and start Django application container
- Automatically create database schema from SQL scripts
- Run Django migrations with `--fake-initial` flag
- Start the development server on port 8000

2. **Wait for services to be ready**:

The application will be available once both containers are healthy. You can check the status:

```bash
make docker-logs
```

Or manually:
```bash
cd infra && docker-compose ps
```

This will:
- Start PostgreSQL database (automatically runs SQL migrations from `init-db/`)
- Build and start Django application
- Run Django migrations automatically (with `--fake-initial` since schema is created by SQL)
- Make the app available at `http://localhost:8000`

**Note**: Database schema is initialized from SQL scripts in `infra/init-db/` when PostgreSQL starts for the first time.

3. **Verify the application is running**:

Open your browser and navigate to `http://localhost:8000/`

You should see the TODO application homepage. You can:
- Create new TODOs by clicking "+ New"
- Edit existing TODOs
- Mark TODOs as resolved
- Delete TODOs

To access the admin panel, go to `http://localhost:8000/admin/` (requires superuser account).

4. **View logs**:

```bash
make docker-logs
```

Or manually:
```bash
cd infra && docker-compose logs -f todo-app
```

5. **Stop services**:

```bash
make docker-down
```

Or manually:
```bash
cd infra && docker-compose down
```

6. **Create superuser** (in Docker container):

```bash
make docker-createsuperuser
```

Or manually:
```bash
cd infra && docker-compose exec todo-app python manage.py createsuperuser
```

## Running Tests

The project includes comprehensive test coverage for models, views, and forms. Tests automatically use SQLite in-memory database, so you don't need PostgreSQL running locally.

### Local Testing

**Quick way (using Makefile):**
```bash
make test
```

**With verbose output:**
```bash
make test-verbose
```

**Manual way:**
```bash
uv run python manage.py test
```

**Run specific test class:**
```bash
uv run python manage.py test todos.tests.TodoModelTest
```

**Run specific test method:**
```bash
uv run python manage.py test todos.tests.TodoModelTest.test_todo_creation
```

**Run tests for specific app:**
```bash
uv run python manage.py test todos
```

### Testing in Docker

If you want to run tests in the Docker container:

```bash
make docker-test
```

Or manually:
```bash
cd infra && docker-compose exec todo-app python manage.py test
```

### Test Coverage

The test suite includes:
- **Model tests**: Todo creation, string representation, overdue logic
- **View tests**: All CRUD operations (create, read, update, delete, toggle)
- **Form tests**: Form validation and error handling

All tests should pass. If any test fails, check the error message and fix the issue.

## Makefile Commands

The project includes a Makefile for common tasks. Run `make help` to see all available commands:

### Local Development
```bash
make help              # Show all available commands
make install           # Install dependencies using uv
make test              # Run tests
make test-verbose      # Run tests with verbose output
make run               # Run development server
make migrate           # Run database migrations
make makemigrations    # Create new migrations
make shell             # Open Django shell
make createsuperuser   # Create Django superuser
make collectstatic     # Collect static files
make clean             # Clean Python cache files
```

### Docker Commands
```bash
make docker-up         # Start Docker containers
make docker-down       # Stop Docker containers
make docker-logs       # View Docker logs
make docker-test       # Run tests in Docker
make docker-shell      # Open shell in Docker container
make docker-migrate    # Run migrations in Docker
make docker-createsuperuser  # Create superuser in Docker
make docker-restart    # Restart Docker containers
make docker-rebuild    # Rebuild Docker containers
make docker-clean      # Remove containers and volumes
```

## Project Structure

```
homework1/
├── manage.py
├── pyproject.toml      # Project dependencies (uv)
├── Makefile            # Convenience commands
├── Dockerfile
├── env.example
├── AGENTS.md           # AI agent instructions
├── todo_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── todos/                  # TODO app
│   ├── __init__.py
│   ├── models.py          # Todo model
│   ├── views.py           # View functions
│   ├── forms.py           # Form classes
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   ├── tests.py           # Test cases
│   └── migrations/         # Django migrations (for local dev)
│       ├── __init__.py
│       └── 0001_initial.py
├── templates/             # HTML templates
│   ├── base.html
│   └── todos/
│       ├── home.html
│       ├── todo_form.html
│       └── todo_confirm_delete.html
└── infra/                 # Docker infrastructure
    ├── docker-compose.yml
    └── init-db/           # SQL migration scripts
        ├── README.md
        └── 01-init.sql   # Initial database schema
```

## Database Migrations

### SQL Migrations (Docker)

When using Docker Compose, database schema is automatically created from SQL scripts located in `infra/init-db/`. These scripts are executed automatically when PostgreSQL container starts for the first time.

The main migration script is `infra/init-db/01-init.sql`, which creates:
- `todos_todo` table with all required fields
- Indexes for optimal query performance:
  - `idx_todos_todo_created_at` - For ordering by creation date
  - `idx_todos_todo_is_resolved` - For filtering resolved/unresolved items
  - `idx_todos_todo_due_date` - For filtering by due date
- Proper permissions for the database user

**Note**: SQL scripts in `/docker-entrypoint-initdb.d/` are only executed when the database is empty (first initialization). If you need to reset the database:

```bash
cd infra
docker-compose down -v  # Removes volumes
docker-compose up -d    # Recreates database and runs init scripts
```

See [infra/init-db/README.md](./infra/init-db/README.md) for more details about SQL migrations.

### Django Migrations (Local Development)

For local development without Docker, Django migrations are used:

```bash
python manage.py migrate
```

To create new migrations after model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Important**: When using Docker, Django migrations are run with `--fake-initial` flag because the initial schema is already created by SQL scripts. This marks migrations as applied without actually running them, since the database structure already exists. This approach:
- Ensures Django's migration tracking is in sync
- Avoids conflicts between SQL scripts and Django migrations
- Maintains consistency across environments

**Note**: Django migrations (`todos/migrations/0001_initial.py`) are still needed for:
- Local development without Docker
- Django's migration tracking system
- Future schema changes (new migrations will be created normally)

## Usage

1. **Create a TODO**: Click "New" button and fill in the form
2. **Edit a TODO**: Click "Edit" on any TODO item
3. **Mark as Resolved**: Click "Resolve" button on a TODO
4. **Delete a TODO**: Click "Delete" button and confirm

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` (requires superuser account).

## Development

This project follows Django best practices:
- MVT (Model-View-Template) architecture
- Function-based views
- Django ORM for database operations
- Form validation
- CSRF protection
- Comprehensive test coverage
- PostgreSQL database
- Docker containerization
- Minimalist UI design

## Environment Variables

The application uses environment variables for database configuration. See `env.example` for available options:

- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL user
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port

**Note**: `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` have default values in `settings.py` and don't need to be set for local development.

## License

This project is part of the AI Dev Tools Zoomcamp course.
