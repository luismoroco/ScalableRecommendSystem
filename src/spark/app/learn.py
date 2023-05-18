from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("VectorSum") \
    .master("spark://spark-master:7077") \
    .getOrCreate()