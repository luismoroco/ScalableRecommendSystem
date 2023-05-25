import os
import argparse
import time
import gc

# spark imports
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, lower
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS


class AlsRecommender:

    def __init__(self, spark_session, path_movies, path_ratings):
        self.spark = spark_session
        self.sc = spark_session.sparkContext
        self.moviesDF = self._load_file(path_movies) \
            .select(['movieId', 'title'])
        self.ratingsDF = self._load_file(path_ratings) \
            .select(['userId', 'movieId', 'rating'])
        self.model = ALS(
            userCol='userId',
            itemCol='movieId',
            ratingCol='rating',
            coldStartStrategy="drop")

    def _load_file(self, filepath):
        return self.spark.read.load(filepath, format='csv',
                                    header=True, inferSchema=True)

    def tune_model(self, maxIter, regParams, ranks, split_ratio=(6, 2, 2)):
        train, val, test = self.ratingsDF.randomSplit(split_ratio)
        self.model = tune_ALS(self.model, train, val,
                              maxIter, regParams, ranks)
        # test model
        predictions = self.model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse",
                                        labelCol="rating",
                                        predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print('The out-of-sample RMSE of the best tuned model is:', rmse)
        del train, val, test, predictions, evaluator
        gc.collect()

    def set_model_params(self, maxIter, regParam, rank):
        self.model = self.model \
            .setMaxIter(maxIter) \
            .setRank(rank) \
            .setRegParam(regParam)

    def matching_movies(self, fav_movie):
        matchesDF = self.moviesDF \
            .filter(
                lower(
                    col('title')
                ).like('%{}%'.format(fav_movie.lower()))
            ) \
            .select('movieId', 'title')
        if not len(matchesDF.take(1)):
            print('Oops! No se encontraron coincidencias')
        else:
            movieIds = matchesDF.rdd.map(lambda r: r[0]).collect()
            titles = matchesDF.rdd.map(lambda r: r[1]).collect()
            print('Se encontraron las siguientes coincidencias en la base de datos: '
                  '{0}\n'.format([x for x in titles]))
            return movieIds

    def append_new_ratings(self, userId, movieIds):
        user_rdd = self.sc.parallelize(
            [(userId, movieId, 5.0) for movieId in movieIds])
        user_rows = user_rdd.map(
            lambda x: Row(
                userId=int(x[0]),
                movieId=int(x[1]),
                rating=float(x[2])
            )
        )
        userDF = self.spark.createDataFrame(user_rows) \
            .select(self.ratingsDF.columns)
        self.ratingsDF = self.ratingsDF.union(userDF)

    def create_inference_data(self, userId, movieIds):
        other_movieIds = self.moviesDF \
            .filter(~col('movieId').isin(movieIds)) \
            .select(['movieId']) \
            .rdd.map(lambda r: r[0]) \
            .collect()

        inferenceRDD = self.sc.parallelize(
            [(userId, movieId) for movieId in other_movieIds]
        ).map(
            lambda x: Row(
                userId=int(x[0]),
                movieId=int(x[1]),
            )
        )

        inferenceDF = self.spark.createDataFrame(inferenceRDD) \
            .select(['userId', 'movieId'])
        return inferenceDF

    def make_inference(self, model, fav_movie, n_recommendations):
        userId = self.ratingsDF.agg({"userId": "max"}).collect()[0][0] + 1
        movieIds = self.matching_movies(fav_movie)
        self.append_new_ratings(userId, movieIds)
        model = model.fit(self.ratingsDF)
        inferenceDF = self.create_inference_data(userId, movieIds)

        return model.transform(inferenceDF) \
            .select(['movieId', 'prediction']) \
            .orderBy('prediction', ascending=False) \
            .rdd.map(lambda r: (r[0], r[1])) \
            .take(n_recommendations)

    def make_recommendations(self, fav_movie, n_recommendations):
        print('Recommendation system start to make inference ...')
        t0 = time.time()
        raw_recommends = \
            self.make_inference(self.model, fav_movie, n_recommendations)
        movieIds = [r[0] for r in raw_recommends]
        scores = [r[1] for r in raw_recommends]
        print('It took my system {:.2f}s to make inference \n\
              '.format(time.time() - t0))

        movie_titles = self.moviesDF \
            .filter(col('movieId').isin(movieIds)) \
            .select('title') \
            .rdd.map(lambda r: r[0]) \
            .collect()

        print('Recommendations for {}:'.format(fav_movie))
        for i in range(len(movie_titles)):
            print('{0}: {1}, with rating '
                  'of {2}'.format(i+1, movie_titles[i], scores[i]))


class Dataset:
    def __init__(self, spark_session, filepath):
        self.spark = spark_session
        self.sc = spark_session.sparkContext
        self.filepath = filepath
        # build spark data object
        self.RDD = self.load_file_as_RDD(self.filepath)
        self.DF = self.load_file_as_DF(self.filepath)

    def load_file_as_RDD(self, filepath):
        ratings_RDD = self.sc.textFile(filepath)
        header = ratings_RDD.take(1)[0]
        return ratings_RDD \
            .filter(lambda line: line != header) \
            .map(lambda line: line.split(",")) \
            .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) # noqa

    def load_file_as_DF(self, filepath):
        ratings_RDD = self.load_file_as_rdd(filepath)
        ratingsRDD = ratings_RDD.map(lambda tokens: Row(
            userId=int(tokens[0]), movieId=int(tokens[1]), rating=float(tokens[2]))) # noqa
        return self.spark.createDataFrame(ratingsRDD)


def tune_ALS(model, train_data, validation_data, maxIter, regParams, ranks):
    min_error = float('inf')
    best_rank = -1
    best_regularization = 0
    best_model = None
    for rank in ranks:
        for reg in regParams:
            als = model.setMaxIter(maxIter).setRank(rank).setRegParam(reg)
            model = als.fit(train_data)
            predictions = model.transform(validation_data)
            evaluator = RegressionEvaluator(metricName="rmse",
                                            labelCol="rating",
                                            predictionCol="prediction")
            rmse = evaluator.evaluate(predictions)
            print('{} latent factors and regularization = {}: '
                  'validation RMSE is {}'.format(rank, reg, rmse))
            if rmse < min_error:
                min_error = rmse
                best_rank = rank
                best_regularization = reg
                best_model = model
    print('\nThe best model has {} latent factors and '
          'regularization = {}'.format(best_rank, best_regularization))
    return best_model


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Movie Recommender",
        description="Run ALS Movie Recommender")
    
    parser.add_argument('--path', nargs='?', default='../app',
                        help='input data path')
    parser.add_argument('--movies_filename', nargs='?', default='movies.csv',
                        help='provide movies filename')
    parser.add_argument('--ratings_filename', nargs='?', default='ratings.csv',
                        help='provide ratings filename')
    parser.add_argument('--movie_name', nargs='?', default='',
                        help='provide your favoriate movie name')
    parser.add_argument('--top_n', type=int, default=10,
                        help='top n movie recommendations')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    data_path = args.path
    movies_filename = args.movies_filename
    ratings_filename = args.ratings_filename
    movie_name = args.movie_name
    top_n = args.top_n

    spark = SparkSession \
        .builder \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Recommender system
    recommender = AlsRecommender(
        spark,
        os.path.join(data_path, movies_filename),
        os.path.join(data_path, ratings_filename))

    recommender.set_model_params(10, 0.05, 20)
    recommender.make_recommendations(movie_name, top_n)
    # stop
    spark.stop()