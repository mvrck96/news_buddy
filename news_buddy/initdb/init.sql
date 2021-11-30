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

CREATE TABLE IF NOT EXISTS sources(source varchar PRIMARY KEY, link VARCHAR);

insert INTO sources(source, link) values ('tass', 'https://tass.ru/');
insert INTO sources(source, link) values ('rbc', 'https://www.rbc.ru/');
insert INTO sources(source, link) values ('gazeta', 'https://www.gazeta.ru/');
insert INTO sources(source, link) values ('habr', 'https://habr.com/');