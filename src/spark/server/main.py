import os
import argparse
import time
import gc

from pyspark.sql import SparkSession, Row
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS

from flask import Flask
from engine.engine import ALSEngineAdapter

from spark.spark import SparkInstancer

spark_session = SparkInstancer()
sc = spark_session.getInstance()

QueryEngine = ALSEngineAdapter('ALSMODEL', sc)

"""x = QueryEngine.getRecommForSpecificUser(10, 10)
x.show()
"""
y = QueryEngine.getNItemsForItem(35, 10)
y.show()


y.foreach(lambda row: print("Movie ID:", row.movieId, "Recommendations:", row.recommendations))


spark_session.shutdown()

"""app = Flask(__name__)


@app.route('/')
def hello_geek():
    return '<h1> Hello from Flask & Docker in Spark </h2>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)"""
  