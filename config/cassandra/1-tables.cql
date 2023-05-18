USE devTest;

CREATE TABLE IF NOT EXISTS genres (
  id INT PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXIST movies (
  id INT PRIMARY KEY,
  title TEXT,
  genres_ids SET<INT>
);