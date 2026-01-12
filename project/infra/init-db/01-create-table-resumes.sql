-- Create resumes table
-- This table stores uploaded resume files (PDF and TXT)

CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    filename VARCHAR NOT NULL,
    original_filename VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL CHECK (file_type IN ('pdf', 'txt')),
    file_path VARCHAR NOT NULL,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for resumes table
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_resumes_file_type ON resumes(file_type);
CREATE INDEX IF NOT EXISTS idx_resumes_updated_at ON resumes(updated_at DESC) WHERE updated_at IS NOT NULL;

