# Database Initialization Scripts

This directory contains SQL scripts that are automatically executed when the PostgreSQL container starts for the first time.

## How It Works

PostgreSQL Docker image automatically executes all `.sql` files in `/docker-entrypoint-initdb.d/` directory when the database is initialized (i.e., when the data directory is empty).

## Scripts

### `01-init.sql`

Creates the initial database schema for the TODO application:

- **Table**: `todos_todo` - Main table for storing TODO items
- **Indexes**: 
  - `idx_todos_todo_created_at` - For ordering by creation date
  - `idx_todos_todo_is_resolved` - For filtering resolved/unresolved items
  - `idx_todos_todo_due_date` - For filtering by due date

## Schema Structure

```sql
todos_todo
├── id (BIGSERIAL PRIMARY KEY)
├── title (VARCHAR(200) NOT NULL)
├── description (TEXT)
├── due_date (TIMESTAMP WITH TIME ZONE)
├── is_resolved (BOOLEAN DEFAULT FALSE)
├── created_at (TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)
└── updated_at (TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)
```

## Resetting the Database

To reset the database and re-run initialization scripts:

```bash
docker-compose down -v  # Removes volumes (deletes all data)
docker-compose up -d    # Recreates database and runs init scripts
```

## Adding New Migrations

To add new SQL migrations:

1. Create a new `.sql` file with a numbered prefix (e.g., `02-add-column.sql`)
2. Place it in this directory
3. The scripts will be executed in alphabetical order
4. Restart the database container (or remove volumes and recreate)

**Important**: These scripts only run when the database is empty. For existing databases, you'll need to manually run SQL scripts or use Django migrations.





