from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local[*]").setAppName("MovieRatings")
sc = SparkContext(conf=conf)

lines = sc.textFile("file:///opt/spark-data/ml-100k/u.data")
ratings = lines.map(lambda x: x.split()[2])
result = ratings.countByValue()

sortedResults = collections.OrderedDict(sorted(result.items()))
for k, v in sortedResults.items():
    print(k, v)
