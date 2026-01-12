# PostgreSQL Database Initialization Scripts

This directory contains SQL scripts for initializing the PostgreSQL database.

## Database Configuration

- **Database Name**: `resume_review`
- **User**: `resume_review`
- **Password**: `resume_review_password` (change in production!)
- **Port**: `5432`

## Files

### Table Creation Scripts (Optional - Manual Table Creation)
- `01-create-table-resumes.sql` - Creates resumes table with indexes (must be first)
- `02-create-table-evaluations.sql` - Creates evaluations table with indexes (depends on resumes)
- `03-create-table-chat-messages.sql` - Creates chat_messages table with indexes (depends on resumes)

**Note**: Each table script includes its own indexes. No additional initialization scripts needed.

## How Tables Are Created

**By Default (Recommended)**: Tables are created automatically by **SQLAlchemy** when the backend application starts:
- See `backend/app/main.py`: `Base.metadata.create_all(bind=engine)`
- This happens when you run: `uv run uvicorn app.main:app --reload`
- Or when Docker Compose starts the backend service

**Alternative**: You can create tables manually using SQL:
- Use individual table creation scripts (executed in order):
  - `01-create-table-resumes.sql` (must be first)
  - `02-create-table-evaluations.sql` (depends on resumes)
  - `03-create-table-chat-messages.sql` (depends on resumes)
- Each script creates one table with its indexes
- Comment out `Base.metadata.create_all` in `backend/app/main.py`
- Tables will be created when PostgreSQL container starts (scripts run in alphabetical order)

**Which approach to use?**
- **SQLAlchemy (default)**: Better for development, easier migrations with Alembic
- **SQL scripts**: Better for production, more control, version-controlled schema

## Usage

These scripts are automatically executed by PostgreSQL when the container starts for the first time. The `docker-compose.yml` mounts this directory to `/docker-entrypoint-initdb.d/` in the PostgreSQL container.

**Important**: Scripts run only on the first initialization. To re-run scripts, you need to remove the PostgreSQL volume:
```bash
docker-compose down -v
docker-compose up db
```

## Script Execution Order

Scripts are executed in alphabetical order when PostgreSQL container starts:
1. `01-create-table-resumes.sql` - Creates resumes table with indexes (must be first)
2. `02-create-table-evaluations.sql` - Creates evaluations table with indexes (depends on resumes)
3. `03-create-table-chat-messages.sql` - Creates chat_messages table with indexes (depends on resumes)

## Adding New Scripts

1. Create a new SQL file with a numeric prefix (e.g., `03-seed-data.sql`)
2. Scripts are executed in alphabetical order
3. Make sure scripts are idempotent (can be run multiple times safely)
4. Use `IF NOT EXISTS` clauses where possible

## Manual Execution

To run scripts manually:

```bash
# Connect to database
docker-compose exec db psql -U resume_review -d resume_review

# Or run a specific script
docker-compose exec db psql -U resume_review -d resume_review -f /docker-entrypoint-initdb.d/01-create-table-resumes.sql
```

## Local PostgreSQL Setup

If running PostgreSQL locally (not in Docker):

```bash
# Create database
createdb -U postgres resume_review

# Run initialization scripts
psql -U resume_review -d resume_review -f 01-create-table-resumes.sql
psql -U resume_review -d resume_review -f 02-create-table-evaluations.sql
psql -U resume_review -d resume_review -f 03-create-table-chat-messages.sql
```
