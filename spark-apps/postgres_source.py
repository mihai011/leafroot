"""Postgress import source
"""
from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import col, desc, count, when

spark = SparkSession.builder.appName("Postgress app").getOrCreate()

jdbcDF1 = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://db/app")
    .option("dbtable", "public.users")
    .option("user", "postgres")
    .option("password", "pass")
    .load()
)

jdbcDF1.show()
