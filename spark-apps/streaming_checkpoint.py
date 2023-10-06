"""
Streaming Check point
"""

from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder.appName("streaming checkpoint").getOrCreate()

ds = spark.readStream.text("/opt/spark-data/text_stream/data_stream")

sq = (
    ds.writeStream.format("text")
    .outputMode("append")
    .option("checkpointLocation", "/opt/spark-data/text_stream/checkpoint")
    .option("path", "/opt/spark-data/text_stream/result")
    .trigger(processingTime="4 seconds")
    .start()
)

sq.awaitTermination()
