-- Initialisation script for database
DROP TABLE IF EXISTS digests;

CREATE TABLE digests (
  id serial,
  title varchar,
  link varchar,
  PRIMARY KEY(id)
);

CREATE TABLE users(id serial, name varchar, PRIMARY KEY(id));
