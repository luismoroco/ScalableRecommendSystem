# spark classes and funcs

from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors

# Crea una sesión de Spark
spark = SparkSession.builder \
    .appName("VectorSum") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

matrix1 = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]]

matrix2 = [[9, 8, 7],
           [6, 5, 4],
           [3, 2, 1]]

rdd1 = spark.sparkContext.parallelize(matrix1)
rdd2 = spark.sparkContext.parallelize(matrix2)

result_rdd = rdd1.zip(rdd2).map(lambda x: [sum(pair) for pair in zip(x[0], x[1])])

result = result_rdd.collect()

print(result)

# Detiene la sesión de Spark
spark.stop()