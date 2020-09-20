CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    username VARCHAR(25) NOT NULL,
    password TEXT NOT NULL
);