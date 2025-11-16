-- Enable UUID generation (use one of these extensions; uuid-ossp is common)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TABLES
CREATE TABLE IF NOT EXISTS initial (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_attribute TEXT NOT NULL,
    some_text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);