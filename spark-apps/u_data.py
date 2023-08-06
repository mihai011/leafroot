from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct

import collections


def print_line_rdd(line):
    print(line, len(line))


conf = SparkConf().setMaster("spark://spark:7077").setAppName("MovieRatings")
# conf = SparkConf().setMaster("local").setAppName("MovieRatings")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
spark.sparkContext.setLogLevel("WARN")

lines_rdd = sc.textFile("file:///opt/spark-data/ml-100k/u.data")
print("Partitions:", lines_rdd.getNumPartitions())
# Getting a dataframe from a RDD.
lines_rdd.foreach(print_line_rdd)
lines_rdd = lines_rdd.map(lambda line: line.split())
lines_rdd.foreach(print_line_rdd)
lines_df = lines_rdd.toDF(["client_id", "movie_id", "rating", "timestamp"])
lines_df.show()

# Simple operations on a rdd
ratings = lines_rdd.map(lambda x: x[2])
result_rdd = ratings.countByValue()
sortedResults = collections.OrderedDict(sorted(result.items()))
for k, v in sortedResults.items():
    print(k, v)

# Simple operations on a DataFrame
result_df = lines_df.groupBy("rating").count().sort("rating")
result.show()
