# spark classes and funcs

from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors

# Crea una sesión de Spark
spark = SparkSession.builder \
    .appName("VectorSum") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Crea un RDD distribuido con el vector de números
vector_size = 1000000
vector_rdd = spark.sparkContext.parallelize(range(vector_size), numSlices=2)

# Convierte el RDD en un DataFrame
df = spark.createDataFrame(vector_rdd.map(lambda x: (Vectors.dense(x),)), ["features"])

# Realiza la suma de los vectores distribuidos
result = df.select(df.features).rdd.reduce(lambda x, y: (x[0] + y[0],))

# Imprime el resultado de la suma
print("Resultado de la suma:", result[0])

# Detiene la sesión de Spark
spark.stop()