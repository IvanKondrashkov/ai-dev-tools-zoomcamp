For MCP development, use `uv` for dependency management.

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

# Run the MCP server
uv run python main.py

# Run tests
uv run python test.py
uv run python search.py
```

## Makefile

The project includes a Makefile for convenience. See `make help` for all available commands.

Common commands:
- `make install` - Install dependencies
- `make test` - Run tests
- `make run` - Start development server
- `make test-scrape` - Test web scraping functionality
- `make test-search` - Test search functionality
- `make clean` - Clean generated files and caches