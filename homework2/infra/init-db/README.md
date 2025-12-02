# Database Initialization Scripts

This directory contains scripts for initializing the PostgreSQL database.

## Files

- `01-init.sql` - Creates database schema (tables, indexes, triggers)
- `02-seed.sql` - Optional seed data (currently empty)

## How It Works

PostgreSQL automatically executes SQL scripts in `/docker-entrypoint-initdb.d/` when the container is first created (when the data directory is empty).

**Note:** Python migrations are handled automatically by the backend application via SQLAlchemy's `Base.metadata.create_all()` in the `lifespan` event handler.

### Execution Order

1. `01-init.sql` - Creates tables and schema
2. `02-seed.sql` - Inserts seed data (if any)

**Note:** These scripts only run when the database is first initialized. If you need to re-run them, you must remove the PostgreSQL volume:

```bash
docker-compose down -v
docker-compose up
```

## Database Schema

### `sessions` table

Stores coding session information:

- `session_id` (VARCHAR, PRIMARY KEY) - Unique session identifier
- `code` (TEXT) - Current code in the editor
- `language` (VARCHAR) - Programming language (javascript, python, go, java)
- `created_at` (TIMESTAMP) - When session was created
- `updated_at` (TIMESTAMP) - Last update time (auto-updated by trigger)

### `code_history` table

Optional table for tracking code changes over time:

- `id` (SERIAL, PRIMARY KEY) - Auto-incrementing ID
- `session_id` (VARCHAR, FOREIGN KEY) - References sessions table
- `code` (TEXT) - Code snapshot
- `language` (VARCHAR) - Language at time of change
- `changed_at` (TIMESTAMP) - When change occurred

## Automatic Features

- **Auto-update trigger**: `updated_at` is automatically updated when a session is modified
- **Indexes**: Created on `created_at`, `updated_at`, and `session_id` for faster queries

