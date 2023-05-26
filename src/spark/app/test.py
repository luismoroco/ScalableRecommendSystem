import os 
from pyspark.ml.recommendation import ALSModel

from pyspark.sql import SparkSession, Row

path = os.path.dirname(os.path.abspath(__file__))

spark = SparkSession \
        .builder \
        .master("spark://spark-master:7077") \
        .getOrCreate()

model = ALSModel.load(os.path.join(path,'ALSMODEL'))

recs = model.recommendForUserSubset(spark.createDataFrame([(9878, )]).toDF('userId'), 10)

spark.stop()

