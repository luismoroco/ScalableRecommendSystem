from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from dotenv import load_dotenv
import os
import gc

load_dotenv()

"""
    -------------------- DATA STORAGE INTO CASSANDRA ----------------------
"""

script_dir = os.path.dirname(os.path.abspath(__file__))

movies_csv_path = os.path.join(script_dir, '..', '..', 'data', 'preprocessed', 'movies_cleaned.csv')
user_rat_csv_path = os.path.join(script_dir, '..', '..', 'data', 'preprocessed', 'users_ratings.csv')

movies_df = pd.read_csv(movies_csv_path)
users_rat_df = pd.read_csv(user_rat_csv_path)
gc.collect()

print("SAVING ... MOVIES INTO CASSANDRA")

genre_dict = {
    'Documentary': 1,
    'Adventure': 2,
    'Sci-Fi': 3,
    'Children': 4,
    'IMAX': 5,
    'Mystery': 6,
    'Animation': 7,
    'War': 8,
    'Drama': 9,
    'Romance': 10,
    'Crime': 11,
    'Action': 12,
    'Musical': 13,
    'Fantasy': 14,
    'Horror': 15,
    'Film-Noir': 16,
    'Comedy': 17,
    '(no genres listed)': 18,
    'Thriller': 19,
    'Western': 20
    }

cluster = Cluster(
    port=int(os.environ['C_NODE1_EXP_PORT']), 
    auth_provider=PlainTextAuthProvider(username=str(os.environ['C_USERNAME']), password=str(os.environ['C_CLUSTER_PASS'])))

session = cluster.connect()

session.set_keyspace(str(os.environ['C_DB_NAME']))

for index, row in movies_df.iterrows():
    idg = {genre_dict.get(gen) for gen in row['genres'].split('|')}
    session.execute("INSERT INTO movies (id, title, count_rat, tmdbId, rat_avg, genres_ids) VALUES (%s, %s, %s, %s, %s, %s)", (row['movieId'], row['title'], row['rating_count'], row['tmdbId'], row['rating_avg'], idg))
gc.collect()


for index, row in users_rat_df.iterrows():
    idMovs = {item for item in row['moviesIds'].split(' ')}
    session.execute("INSERT INTO users (id, count_rat, avg_rat, mov_rateds) VALUES (%s, %s, %s, %s)", (row['userId'], row['count_rat'], row['avg_rat'], idMovs))
gc.collect()

session.shutdown()

print("DATA SAVED IN CASSANDRAA CLUSTER!")