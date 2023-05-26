import os 
import math
from pyspark.ml.recommendation import ALSModel

from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.ml.recommendation import ALS

path = os.path.dirname(os.path.abspath(__file__))

ERR_READ = 'Error while trying to read file'

class ALSRecommender:
    model = None
    spark = None
    maxIter = None
    rank = None
    reg = None
    df = None
    train = None
    test = None
    val = None

    def __init__(self, sc, it, rk, rg) -> None:
        self.spark = sc
        self.maxIter = it
        self.rank = rk
        self.reg = rg

    def readFiles(self, name: str) -> None:
        try:
             self.df = self.spark.read.csv(os.path.join(path, name), inferSchema=True, header=True)
        except:
             raise Exception(ERR_READ)

    def partition(self) -> None:
        self.train, self.test, self.val = self.df.randomSplit([0.6, 0.2, 0.2])


    def fit(self) -> None:
        self.partition()
        self.model = ALS(userCol='userId', ratingCol='rating', itemCol='movieId')
        self.model.setMaxIter(self.maxIter).setRank(self.rank).setRegParam(self.reg)
        self.model = self.model.fit(self.train)
 
    def save(self) -> None:
        self.model.save(os.path.join(path, 'ALSMODEL_2'))


"""spark = SparkSession \
        .builder \
        .master("spark://spark-master:7077") \
        .getOrCreate()

from pyspark.ml.recommendation import ALS

df = spark.read.csv(os.path.join(path, 'ratings.csv'), inferSchema=True, header=True)
df.head(10)

train, test, val = df.randomSplit([0.6, 0.2, 0.2])

mod = ALS(userCol='userId', ratingCol='rating', itemCol='movieId')
#mod = ALS(userCol='userId', ratingCol='rating', itemCol='movieId', iter=10, rank=20, regParam=20)

als = mod.setMaxIter(10).setRank(20).setRegParam(0.05)

mod = als.fit(train)

#mod.save(os.path.join(path, 'ALSMODEL'))

preds = mod.transform(val)

preds.show()

#preds = preds.filter(preds.prediction.isNotNull() & preds.rating.isNotNull())

evaluator = RegressionEvaluator(metricName='rmse', labelCol='rating', predictionCol='prediction')
rmse = evaluator.evaluate(preds)
print("RMSE: {}".format(rmse))


test.show()

test.filter(test['userId'] == 45).show()

user_1 = test.filter(test['userId'] == 45)

user_1.show()

recomendation = mod.transform(user_1)

recomendation.orderBy('prediction', ascending=False).show()

spark.stop()"""