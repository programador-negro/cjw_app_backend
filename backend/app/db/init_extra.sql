-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    start_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- People Table
CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    contact_name VARCHAR(100),
    contact_phone VARCHAR(50),
    has_whatsapp BOOLEAN DEFAULT FALSE,
    address TEXT,
    congregation VARCHAR(100),
    user_id INTEGER REFERENCES users(id),
    current_level VARCHAR(100)
);

-- Assignments Table
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    assignment_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assignment_part VARCHAR(255),
    created_by INTEGER REFERENCES users(id),
    room_number INTEGER,
    additional_notes TEXT,
    assignment_sent BOOLEAN DEFAULT FALSE
);

-- Privileges Table
CREATE TABLE IF NOT EXISTS privileges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    privilege_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    privilege_part VARCHAR(255),
    created_by INTEGER REFERENCES users(id),
    room_number INTEGER,
    additional_notes TEXT,
    privilege_sent BOOLEAN DEFAULT FALSE
);

-- Insert example users with bcrypt hashed passwords
-- admin123 hashed
-- user123 hashed

INSERT INTO users (name, email, password, role) VALUES
    ('Admin User', 'admin@example.com', '$2b$12$tGZZqZqz5kFTaZW6RzGU8e9MyZIzNiPWR/qr4/R/UTzwbDXdQHNcS', 'admin'),
    ('Test User', 'user@example.com', '$2b$12$6tCL5P8bK/8nTQhGf3p9KOxjH4rbzYuS0IpRQFJCFMnkJ1JdJV/h2', 'user');
