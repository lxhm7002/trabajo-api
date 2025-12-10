CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    encrypted_password BLOB NOT NULL 
);

CREATE TABLE IF NOT EXISTS todos (
    userId INTEGER,
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS eliminadas (
    id INTEGER PRIMARY KEY
);
