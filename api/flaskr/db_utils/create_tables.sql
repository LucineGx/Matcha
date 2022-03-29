CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar(32) UNIQUE NOT NULL,
    firstname varchar(32) NOT NULL,
    lastname varchar(32) NOT NULL,
    password varchar(32) NOT NULL,
    confirmed INTEGER NOT NULL DEFAULT 0,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    confirmation_token varchar(32),
    password_reinit_token varchar(32)
);

CREATE TABLE IF NOT EXISTS tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) UNIQUE NOT NULL,
    color CHAR(7) NOT NULL
)