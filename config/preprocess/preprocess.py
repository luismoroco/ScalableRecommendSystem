import pandas as pd
import os
from lib import exportFile, exportSpark
import gc
from dotenv import load_dotenv

load_dotenv()

# MOVIES CLEANING
print("Cleaning ... MOVIES")

script_dir = os.path.dirname(os.path.abspath(__file__))
movies_csv_path = os.path.join(script_dir, '..', '..', 'data', 'ml-latest', 'movies.csv')
ratings_csv_path = os.path.join(script_dir, '..', '..', 'data', 'ml-latest', 'ratings.csv')

movies_df = pd.read_csv(movies_csv_path, usecols=['movieId', 'title', 'genres'])
rating_df = pd.read_csv(ratings_csv_path)

movies_df.drop_duplicates(inplace=True)

movies_without_ratings = movies_df[~movies_df['movieId'].isin(rating_df['movieId'])]
movies_without_ratings_rows = movies_without_ratings[['movieId', 'title']]

print('MOVIES WITHOUT RATINGS:', movies_without_ratings_rows.shape)

movies_cleaned = movies_df[~movies_df['movieId'].isin(movies_without_ratings_rows['movieId'])]

print('CLEANED MOVIES CSV:', movies_df.shape, '->' ,movies_cleaned.shape)

exportFile(movies_cleaned, 'movies_cleaned')

print('CLEANED_MOVIES EXPORTED!')

# DATA STORAGE 
"""
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

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cluster = Cluster(
    port=int(os.environ['C_NODE1_EXP_PORT']), 
    auth_provider=PlainTextAuthProvider(username=str(os.environ['C_USERNAME']), password=str(os.environ['C_CLUSTER_PASS'])))

session = cluster.connect()

session.set_keyspace(str(os.environ['C_DB_NAME']))

for index, row in movies_cleaned.iterrows():
    idg = {genre_dict.get(gen) for gen in row['genres'].split('|')}
    session.execute("INSERT INTO movies (id, title, genres_ids) VALUES (%s, %s, %s)", (row['movieId'], row['title'], idg))

session.shutdown()

print("DATA SAVED IN CASSANDRAA CLUSTER!")"""

# RATING

rating_df.drop('timestamp', axis=1, inplace=True)

exportSpark(rating_df, 'ratings')

gc.collect()