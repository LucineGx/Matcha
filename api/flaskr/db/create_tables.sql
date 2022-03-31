CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar(32) UNIQUE NOT NULL,
    first_name varchar(32) NOT NULL,
    last_name varchar(32) NOT NULL,
    password varchar(32) NOT NULL,
    confirmed TINYINT NOT NULL DEFAULT 0,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    confirmation_token varchar(32),
    password_reinit_token varchar(32)
);

CREATE TABLE IF NOT EXISTS tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) UNIQUE NOT NULL,
    color CHAR(7) NOT NULL
);

CREATE TABLE IF NOT EXISTS profile (
    user_id INTEGER PRIMARY KEY,
    gender varchar(6) DEFAULT 'none',
    search_male TINYINT NOT NULL DEFAULT 1,
    search_female TINYINT NOT NULL DEFAULT 1,
    search_none TINYINT NOT NULL DEFAULT 1,
    short_bio varchar(280),
    public_popularity_score TINYINT,
    type varchar(8) NOT NULL,
    type_2 varchar(8),
    egg_group varchar(12),
    egg_group_2 varchar(12),
    'level' TINYINT NOT NULL
);