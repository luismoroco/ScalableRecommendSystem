from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.mllib.linalg.distributed import CoordinateMatrix

import os

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("VectorSum") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, 'ratings.csv')

df = spark.read.csv(path, header=True, inferSchema=True)


"""rdd = df.rdd.map(lambda row: (row[0], row[1], row[2])).cache()

coordinates = rdd.map(lambda x: (x[0], x[1], x[2]))
matrix = CoordinateMatrix(coordinates)"""

train, test = df.randomSplit([0.8, 0.2])

recommerder = ALS(userCol='userId', ratingCol='rating', itemCol='movieId')
recommerder.fit(train)

spark.stop()
