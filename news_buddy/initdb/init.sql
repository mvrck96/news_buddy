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

CREATE TABLE IF NOT EXISTS keywords(
  word varchar,
  TABLE varchar,
  time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sources(source varchar PRIMARY KEY, link VARCHAR);

INSERT INTO sources(source, link)
VALUES ('tass', 'https://tass.ru/');

INSERT INTO sources(source, link)
VALUES ('rbc', 'https://www.rbc.ru/');

INSERT INTO sources(source, link)
VALUES ('gazeta', 'https://www.gazeta.ru/');

INSERT INTO sources(source, link)
VALUES ('habr', 'https://habr.com/');

