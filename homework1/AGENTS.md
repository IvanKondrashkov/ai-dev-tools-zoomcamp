For backend development, use `uv` for dependency management.

## Installation

Install `uv` if not already installed:
```bash
pip install uv
```

## Useful Commands

### Dependency Management
```bash
# Sync dependencies from pyproject.toml
uv sync

# Add a new package
uv add <PACKAGE-NAME>

# Remove a package
uv remove <PACKAGE-NAME>

# Update all dependencies
uv sync --upgrade
```

### Running Commands
```bash
# Run Python files
uv run python <PYTHON-FILE>

# Run Django management commands
uv run python manage.py <command>

# Run tests
uv run python manage.py test
```

## Makefile

The project includes a Makefile for convenience. See `make help` for all available commands.

Common commands:
- `make install` - Install dependencies
- `make test` - Run tests
- `make run` - Start development server
- `make migrate` - Run migrations