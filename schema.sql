CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    username VARCHAR(25) UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP,
    user_id INTEGER REFERENCES users,
);
CREATE TABLE rooms(
    id SERIAL PRIMARY KEY, 
    room_name VARCHAR(40) NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE room_messages(
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms,
    message_id INTEGER REFERENCES messages
);
CREATE TABLE rooms_users(
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms,
    user_id INTEGER REFERENCES users,
    rights INTEGER NOT NULL
);