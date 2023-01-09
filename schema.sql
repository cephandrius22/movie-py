CREATE TABLE IF NOT EXISTS movies (
  budget  INTEGER,
  title   TEXT,
  release_date  DATE,
  runtime INTEGER,
  id      INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS actor_credits (
  character TEXT,
  name TEXT,
  id INTEGER,
  movie_id INTEGER,
  credit_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS crew_credits (
  job TEXT,
  department TEXT,
  name TEXT,
  movie_id INTEGER,
  credit_id INTEGER PRIMARY KEY
);