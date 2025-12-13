-- Enable UUID generation (use one of these extensions; uuid-ossp is common)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TodoStatus Table
CREATE TABLE IF NOT EXISTS todo_statuses (
	id SERIAL PRIMARY KEY,
	value VARCHAR(50) NOT NULL
);

-- Insert TodoStatus values
INSERT INTO todo_statuses (value) VALUES ('pending') ON CONFLICT DO NOTHING;
INSERT INTO todo_statuses (value) VALUES ('in_progress') ON CONFLICT DO NOTHING;
INSERT INTO todo_statuses (value) VALUES ('completed') ON CONFLICT DO NOTHING;

-- TodoPriority Table
CREATE table if not exists todo_priorities (
	id SERIAL PRIMARY KEY,
	value VARCHAR(50) not NULL
);

-- Insert TodoPriority values
INSERT INTO todo_priorities (value) VALUES ('low') ON CONFLICT DO NOTHING;
INSERT INTO todo_priorities (value) VALUES ('medium') ON CONFLICT DO NOTHING;
INSERT INTO todo_priorities (value) VALUES ('high') ON CONFLICT DO NOTHING;

-- TODO Table
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status INT NOT NULL,
    priority INT NOT NULL,
    due_date DATETIME,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (status) REFERENCES todo_statuses(id),
    FOREIGN KEY (priority) REFERENCES todo_priorities(id)f
);

-- Index for better query performance
CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
CREATE INDEX IF NOT EXISTS idx_todos_priority ON todos(priority);
CREATE INDEX IF NOT EXISTS idx_todos_due_date ON todos(due_date);
CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at);