from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext


# conf = SparkConf().setMaster("spark://spark:7077").setAppName("Network Count")
conf = SparkConf().setMaster("local").setAppName("Network COunt")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 1)

lines = ssc.socketTextStream("localhost", 9999)
words = lines.flatMap(lambda line: line.split())

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()

ssc.start()  # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
