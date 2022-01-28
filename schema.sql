CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE averages (id SERIAL PRIMARY KEY, average_date  DATE,  user_id INTEGER REFERENCES users, average REAL);
CREATE TABLE games (id SERIAL PRIMARY KEY, game_date DATE, player_one INTEGER REFERENCES users, player_two INTEGER REFERENCES users, result INTEGER);
