from pyspark.sql import SparkSession
from pyspark.sql.types import *

SPARK_CLOSE='error trying to close spark instance'
SPARK_OPEN='error trying to open spark instance'
SPARK_INSTANCE='erro returning spark instance'

class SparkInstancer:
    spark = None

    def __init__(self) -> None:
        try:
          self.spark = SparkSession \
            .builder \
            .master("spark://spark-master:7077") \
            .getOrCreate()
        except:
          raise Exception(SPARK_OPEN)

    def shutdown(self) -> None:
        try:
          self.spark.stop()
        except:
          raise Exception(SPARK_CLOSE) 
    
    def getInstance(self) -> any:
        try:
          return self.spark
        except:
           raise Exception(SPARK_INSTANCE)