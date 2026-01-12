# Backend Tests

This directory contains unit and integration tests for the backend API.

## Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_models.py      # Database model tests
│   └── test_schemas.py     # Pydantic schema validation tests
└── integration/             # Integration tests
    ├── test_resumes_api.py      # Resume API endpoint tests
    ├── test_evaluations_api.py  # Evaluation API endpoint tests
    └── test_chat_api.py         # Chat API endpoint tests
```

## Running Tests

### Install Test Dependencies

```bash
uv sync --extra test
```

### Run All Tests

```bash
uv run pytest tests/ -v
```

### Run Unit Tests Only

```bash
uv run pytest tests/unit -v
```

### Run Integration Tests Only

```bash
uv run pytest tests/integration -v
```

### Run with Coverage

```bash
uv run pytest tests/ --cov=app --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`

### Run Specific Test File

```bash
uv run pytest tests/unit/test_models.py -v
```

### Run Specific Test

```bash
uv run pytest tests/unit/test_models.py::test_resume_model_creation -v
```

## Test Configuration

Tests use:
- **SQLite in-memory database** for fast test execution
- **TestClient** from FastAPI for API testing
- **Pytest fixtures** for database and client setup
- **Temporary directories** for file upload tests

## Writing Tests

### Unit Tests

Test individual components in isolation:
- Models (database models)
- Schemas (Pydantic validation)
- Utility functions

### Integration Tests

Test API endpoints end-to-end:
- HTTP requests/responses
- Database interactions
- File uploads
- Error handling

## Fixtures

- `db_session`: Fresh database session for each test
- `client`: FastAPI TestClient with database override
- `upload_dir`: Temporary directory for file uploads

