-- Create chat_messages table
-- This table stores real-time chat messages for each resume

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    username VARCHAR NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for chat_messages table
CREATE INDEX IF NOT EXISTS idx_chat_messages_resume_id ON chat_messages(resume_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at ASC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_resume_created ON chat_messages(resume_id, created_at ASC);

