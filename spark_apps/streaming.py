"""Module to demonstrate spark streaming."""

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext


def main() -> None:
    """Main function for spark streaming."""
    conf = SparkConf().setMaster("local").setAppName("Network COunt")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 1)

    lines = ssc.socketTextStream("localhost", 9999)
    words = lines.flatMap(lambda line: line.split())

    # Count each word in each batch
    pairs = words.map(lambda word: (word, 1))
    word_counts = pairs.reduceByKey(lambda x, y: x + y)
    word_counts.pprint()

    ssc.start()  # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate
