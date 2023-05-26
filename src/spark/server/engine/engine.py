import os 
import math
from pyspark.ml.recommendation import ALSModel

path = os.path.dirname(os.path.abspath(__file__))
pathModel = os.path.join(path, '..', '..', 'model')

MOD_CHARGUE='Error while trying to mount model'
QUERY_ERROR='Error while trying to make a query'

class ALSEngineAdapter:
    model = None
    spark = None

    def __init__(self, pathName: str, sparkInstance) -> None:
        self.model = ALSModel.load(os.path.join(pathName))
        self.spark = sparkInstance

        if self.model is not None:
            print('Model {} charget'.format(pathName))
        else:
            raise Exception(MOD_CHARGUE)
    
    def getTopNMoviesForUsers(self, n: int) -> any:
        try:
            recs = self.model.recommendForAllUsers(n)
            return recs
        except:
            raise Exception(QUERY_ERROR)    

    def getRecommForSpecificUser(self, id: int, n: int) -> any:
        try:
            recs = self.model.recommendForUserSubset(self.spark.createDataFrame([(id, )]) \
                                                     .toDF('userId'), n)
            return recs
        except:
            raise Exception(QUERY_ERROR)
    
    def getNItemsForItem(self, id: int, n: int) -> any:
        try:
            recs = self.model.recommendForItemSubset(self.spark.createDataFrame([(id, )]) \
                                                     .toDF("itemId"), n)
            return recs
        except:
            raise Exception(QUERY_ERROR)
        