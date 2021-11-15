-- Initialisation script for newsbuddy_db


CREATE TABLE IF NOT EXISTS news_tass(
  id serial PRIMARY KEY,
  title VARCHAR,
  link VARCHAR,
  time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_rbc(
  id serial PRIMARY KEY,
  title VARCHAR,
  link VARCHAR,
  time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_gazeta(
  id serial PRIMARY KEY,
  title VARCHAR,
  link VARCHAR,
  time TIMESTAMP
);