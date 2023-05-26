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

spark_session.shutdown()










"""from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_geek():
    return '<h1> Hello from Flask & Docker in Spark </h2>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
  
  """