DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    password TEXT NOT NULL,
    confirmed INTEGER NOT NULL DEFAULT 0,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    confirmation_token TEXT,
    password_reinit_token TEXT
);