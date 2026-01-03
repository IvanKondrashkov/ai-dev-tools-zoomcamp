# MCP Server - Documentation Search Engine

A Model Context Protocol (MCP) server that provides tools for web scraping and documentation search. Built with FastMCP and minsearch.

## Features

- ✅ Web scraping using Jina Reader API
- ✅ Documentation search engine with minsearch
- ✅ FastMCP-based MCP server implementation
- ✅ Searchable documentation index from GitHub repositories
- ✅ Integration with AI assistants (Cursor, Claude, etc.)

## Prerequisites

- Python 3.11+
- `uv` package manager (install with `pip install uv`)

## Installation

Install dependencies:

```bash
make install
```

Or manually:

```bash
uv sync
```

## Running the Application

### Start the MCP Server

```bash
make run
```

Or:

```bash
uv run python main.py
```

The server will start and listen for MCP protocol messages via STDIO.

## Testing

### Run all tests

```bash
make test
```

### Run tests separately

```bash
# Test web scraping functionality
make test-scrape

# Test search functionality
make test-search
```

### Manual Testing

You can also run tests directly:

```bash
# Test web scraping
uv run python test.py

# Test search functionality
uv run python search.py
```

## Integration with AI Assistants

To integrate this MCP server with Cursor or other AI assistants:

1. Open your AI assistant settings
2. Find the MCP or Model Context Protocol section
3. Add a new MCP server with:
   - **Name**: homework3 (or any name you prefer)
   - **Command**: `uv --directory <FULL_PATH_TO_HOMEWORK3> run python main.py`
   - **Transport**: STDIO

See [INTEGRATION.md](INTEGRATION.md) for detailed instructions.

## Project Structure

```
homework3/
├── main.py              # MCP server with tools
├── search.py            # Search functionality implementation
├── test.py              # Web scraping tests
├── test_minsearch.py    # Minsearch API tests
├── pyproject.toml       # Project dependencies
├── uv.lock              # Locked dependency versions
├── Makefile             # Build automation
├── INTEGRATION.md       # Integration instructions
└── README.md            # This file
```

## Available Tools

The MCP server provides the following tools:

### `scrape_web`

Scrapes content from any web page using Jina Reader API.

**Parameters:**
- `url` (str): The URL of the web page to scrape

**Returns:**
- Markdown-formatted content of the web page

**Example:**
```python
scrape_web("https://datatalks.club/")
```

### `search_docs`

Searches the indexed fastmcp documentation.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int, optional): Number of results to return (default: 5)

**Returns:**
- List of relevant documents with filename and content

**Example:**
```python
search_docs("demo", num_results=5)
```

### `add`

Simple addition tool for testing (demo tool from FastMCP).

**Parameters:**
- `a` (int): First number
- `b` (int): Second number

**Returns:**
- Sum of the two numbers

## Development

### Adding New Tools

To add a new tool to the MCP server:

1. Define your function in `main.py`
2. Decorate it with `@mcp.tool`
3. Add a docstring for the tool description
4. Restart the MCP server

Example:

```python
@mcp.tool
def my_new_tool(param: str) -> str:
    """Description of what this tool does"""
    return f"Result: {param}"
```

### Dependency Management

The project uses `uv` for dependency management:

```bash
# Add a new package
uv add <PACKAGE-NAME>

# Remove a package
uv remove <PACKAGE-NAME>

# Sync dependencies
uv sync

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

## Makefile Commands

Run `make help` to see all available commands:

- `make install` - Install dependencies
- `make run` - Run the MCP server
- `make test` - Run all tests
- `make test-scrape` - Test web scraping functionality
- `make test-search` - Test search functionality
- `make clean` - Clean generated files and caches

## How It Works

### Web Scraping

The `scrape_web` tool uses Jina Reader API to convert any web page to markdown format. Simply prepend `r.jina.ai/` to any URL to get clean, readable markdown content.

### Documentation Search

The `search_docs` tool:
1. Downloads the fastmcp GitHub repository as a ZIP file (if not already downloaded)
2. Extracts all `.md` and `.mdx` files
3. Indexes them using minsearch (TF-IDF based search)
4. Returns the most relevant documents for a given query

The index is created on first use and cached for subsequent searches.

## License

This project is part of the AI Dev Tools Zoomcamp course.