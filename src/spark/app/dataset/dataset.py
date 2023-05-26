from pyspark.sql import Row

class Dataset:
    def __init__(self, spark, filepath):
        self.spark = spark
        self.sc = spark.sparkContext
        self.filepath = filepath

        self.RDD = self.loadAsRDD(self.filepath)
        self.DF = self.loasAsDF(self.filepath)

    def loadAsRDD(self, filepath):
        ratings_RDD = self.sc.textFile(filepath)
        header = ratings_RDD.take(1)[0]
        return ratings_RDD \
            .filter(lambda line: line != header) \
            .map(lambda line: line.split(",")) \
            .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) 

    def loasAsDF(self, filepath):
        ratings_RDD = self.loadAsRDD(filepath)
        ratingsRDD = ratings_RDD.map(lambda tokens: Row(
            userId=int(tokens[0]), movieId=int(tokens[1]), rating=float(tokens[2]))) 
        return self.spark.createDataFrame(ratingsRDD)

