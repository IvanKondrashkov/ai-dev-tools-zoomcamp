.PHONY: help install run test test-scrape test-search clean

help:
	@echo Available commands:
	@echo   make install      - Install dependencies using uv
	@echo   make run          - Run the MCP server
	@echo   make test         - Run all tests
	@echo   make test-scrape  - Test web scraping functionality
	@echo   make test-search  - Test search functionality
	@echo   make clean        - Clean generated files and caches

install:
	uv sync

run:
	uv run python main.py

test: test-scrape test-search

test-scrape:
	uv run python test.py

test-search:
	uv run python search.py

clean:
	@echo Cleaning...
	rm -rf .venv .uv __pycache__ .pytest_cache
	rm -f *.zip