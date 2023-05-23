import pandas as pd
import os
from lib import exportFile
import gc
from dotenv import load_dotenv

load_dotenv()

from sklearn.preprocessing import StandardScaler
scalerEngine = StandardScaler()

"""
    -------------------- DATA CLEANING ----------------------
"""

print("Cleaning ... MOVIES")

"""
    GETTING PATHS AND READ CSV
"""

script_dir = os.path.dirname(os.path.abspath(__file__))

movies_csv_path = os.path.join(script_dir, '..', '..', 'data', 'ml-latest', 'movies.csv')
ratings_csv_path = os.path.join(script_dir, '..', '..', 'data', 'ml-latest', 'ratings.csv')
links_csv_path = os.path.join(script_dir, '..', '..', 'data', 'ml-latest', 'links.csv')

movies_df = pd.read_csv(movies_csv_path, usecols=['movieId', 'title', 'genres'])
rating_df = pd.read_csv(ratings_csv_path, usecols=['userId', 'movieId', 'rating'])
links_df = pd.read_csv(links_csv_path, usecols=['movieId', 'tmdbId'], dtype={'tmdbId': str})


"""
    STANDARIZING DATA ['RATING]
"""
# FOR MOVIES 

rating_df['rating'] = scalerEngine.fit_transform(rating_df[['rating']])
gc.collect()


"""
    DROP DUPLICATES, DROP MOVIES WITHOUR RATINGS, AVG PER MOVIE AND COUNTING
"""

movies_df.drop_duplicates(inplace=True)

# movie without ratings
movies_without_ratings = movies_df[~movies_df['movieId'].isin(rating_df['movieId'])]
movies_without_ratings_rows = movies_without_ratings[['movieId', 'title']]
print('MOVIES WITHOUT RATINGS:', movies_without_ratings_rows.shape)

# filtering
movies_cleaned = movies_df[~movies_df['movieId'].isin(movies_without_ratings_rows['movieId'])]

# avg per movie
rating_avg = rating_df.groupby('movieId')['rating'].mean().reset_index(name='rating_avg')

# counting
rating_count = rating_df.groupby('movieId').size().reset_index(name='rating_count')

# merge (count, mov, avg)
movies_cleaned = pd.merge(movies_cleaned, rating_count, on='movieId', how='left')
movies_cleaned = pd.merge(movies_cleaned, rating_avg, on='movieId', how='left')
movies_cleaned = pd.merge(movies_cleaned, links_df, on='movieId')
print('CLEANED MOVIES CSV:', movies_df.shape, '->', movies_cleaned.shape)

# export file
exportFile(movies_cleaned, 'movies_cleaned')
print('CLEANED_MOVIES EXPORTED!')
gc.collect()


# FOR USERS AND RATINGS 

count_rat = rating_df.groupby('userId').size().reset_index(name='count_rat')

# avg per user
avg_rat = rating_df.groupby('userId')['rating'].mean().reset_index(name='avg_rat')

# generating list of movies rated
moviesIds = rating_df.groupby('userId')['movieId'].apply(lambda x: ' '.join(x.astype(str))).reset_index(name='moviesIds')

# merge
users_ratings = count_rat.merge(avg_rat, on='userId').merge(moviesIds, on='userId')
exportFile(users_ratings, 'users_ratings')
print('USERS_RATING EXPORTED!')
gc.collect()
