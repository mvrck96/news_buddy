-- Initialisation script for newsbuddy_db

CREATE TABLE IF NOT EXISTS news_tass(
  id serial PRIMARY KEY,
  title TEXT,
  link VARCHAR,
  time TIMESTAMP,
  source VARCHAR DEFAULT 'tass'
);

CREATE TABLE IF NOT EXISTS news_rbc(
  id serial PRIMARY KEY,
  title TEXT,
  link VARCHAR,
  time TIMESTAMP,
  source VARCHAR DEFAULT 'rbc'
);

CREATE TABLE IF NOT EXISTS news_gazeta(
  id serial PRIMARY KEY,
  title TEXT,
  link VARCHAR,
  time TIMESTAMP,
  source VARCHAR DEFAULT 'gazeta'
);