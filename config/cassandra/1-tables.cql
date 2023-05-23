USE devTest;

CREATE TABLE IF NOT EXISTS genres (
  id INT PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS movies (
  id INT PRIMARY KEY,
  title TEXT,
  count_rat INT,
  tmdbId TEXT,
  rat_avg FLOAT,
  genres_ids SET<INT>
);

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY,
  count_rat INT, 
  avg_rat FLOAT,  
  mov_rateds SET<INT> 
);

CREATE TABLE IF NOT EXISTS ratings (
  id INT PRIMARY KEY,
  id_user INT,
  id_movie INT,
  rating FLOAT
);