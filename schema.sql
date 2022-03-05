CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE settings (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, name TEXT, language TEXT);
CREATE TABLE games (id SERIAL PRIMARY KEY, game_date DATE, player_one INTEGER REFERENCES users, player_two INTEGER REFERENCES users, result INTEGER);
CREATE TABLE averages (id SERIAL PRIMARY KEY, game_id INTEGER REFERENCES games, average_date DATE, user_id INTEGER REFERENCES users, average REAL, tons INTEGER, highest_score INTEGER);
