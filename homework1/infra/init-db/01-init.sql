-- Initialize database for Django TODO Application
-- This script is automatically executed when PostgreSQL container starts for the first time
-- Location: /docker-entrypoint-initdb.d/01-init.sql

-- Create todos_todo table
-- This matches the Django model structure
CREATE TABLE IF NOT EXISTS todos_todo (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on created_at for ordering (matches Django model Meta ordering)
CREATE INDEX IF NOT EXISTS idx_todos_todo_created_at ON todos_todo(created_at DESC);

-- Create index on is_resolved for filtering resolved/unresolved todos
CREATE INDEX IF NOT EXISTS idx_todos_todo_is_resolved ON todos_todo(is_resolved);

-- Create index on due_date for filtering by due date
CREATE INDEX IF NOT EXISTS idx_todos_todo_due_date ON todos_todo(due_date) WHERE due_date IS NOT NULL;

-- Grant permissions to todo_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO todo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO todo_user;





