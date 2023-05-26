import gc

from engine.engine import ALSEngineAdapter
from spark.spark import SparkInstancer


spark_session = SparkInstancer()
sc = spark_session.getInstance()


"""mod = ALSRecommender(sc, 10, 20, 0.05)
mod.readFiles('ratings.csv')
mod.fit()
mod.save()
"""

QueryEngine = ALSEngineAdapter('ALSMODEL', sc)

INT_LEN = 15

def displayData(df) -> None:
    rdd_df = df.rdd

    for row in rdd_df.collect():
        print('UserId', row.userId, 'Recomend', row.recommendations, '\n')

def Menu():
    entry: int 
    while True:
        entry = int(input('Input a User ID \n'))
        if entry == -1:
            break

        recs = QueryEngine.getRecommForSpecificUser(entry, INT_LEN)
        recs.show()
        displayData(recs)
        gc.collect()

    spark_session.shutdown()

Menu()


"""app = Flask(__name__)


@app.route('/')
def hello_geek():
    return '<h1> Hello from Flask & Docker in Spark </h2>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)"""
  