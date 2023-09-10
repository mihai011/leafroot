"""This file contains example for sql queries and dataframe api on data from departures.csv file.
"""
from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import col, desc, count, when

spark = SparkSession.builder.appName("SparkSQLExampleApp").getOrCreate()

csv_file = "spark-data/departuredelays.csv"

# Read and create a temporary view # Infer schema (note that for larger files you # may want to specify the schema)
df = (
    spark.read.format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load(csv_file)
)
spark.sparkContext.setLogLevel("WARN")
df.createOrReplaceTempView("us_delay_flights_tbl")

spark.sql(
    """SELECT distance, origin, destination FROM us_delay_flights_tbl WHERE distance > 1000 group by distance, origin, destination
          ORDER BY distance DESC"""
).show(5)

df.select("distance", "origin", "destination").where(
    col("distance") > 1000
).groupBy(col("distance"), col("origin"), col("destination")).count().drop(
    col("count")
).orderBy(
    col("distance").desc()
).show(
    5
)

spark.sql(
    """SELECT date, delay, origin, destination FROM
          us_delay_flights_tbl WHERE delay > 120 AND ORIGIN = 'SFO' AND DESTINATION = 'ORD' ORDER by delay DESC"""
).show(5)

df.select("date", "delay", "origin", "destination").where(
    (col("delay") > 150)
    & (col("destination") == "ORD")
    & (col("origin") == "SFO")
).orderBy(col("delay").desc()).show(5)

spark.sql(
    """SELECT origin, destination, count(*) as delays FROM
          us_delay_flights_tbl group by origin, destination ORDER by delays DESC"""
).show(5)

df.select("origin", "destination").groupBy(
    col("origin"), col("destination")
).agg(count("*").alias("delays")).orderBy(col("delays").desc()).show(5)

spark.sql(
    """SELECT count(*) as total_delays,
        CASE
        WHEN delay > 360 THEN 'Very Long Delays'
        WHEN delay > 120 AND delay < 360 THEN 'Long Delays'
        WHEN delay > 60 AND delay < 120 THEN 'Short Delays'
        WHEN delay > 0 and delay < 60 THEN 'Tolerable Delays'
        WHEN delay = 0 THEN 'No Delays' ELSE 'Early' END AS Flight_Delays
        FROM us_delay_flights_tbl
          group by Flight_Delays
          ORDER BY total_delays DESC"""
).show(10)

df.withColumn(
    "Flight_Delays",
    when((col("delay") > 360), "Very Long Delays")
    .when((col("delay") > 120) & (col("delay") < 360), "Long Delays")
    .when((col("delay") > 60) & (col("delay") < 120), "Short Delays")
    .when((col("delay") > 0) & (col("delay") < 60), "Tolerable Delays")
    .when((col("delay") == 0), "No Delays")
    .otherwise("Early"),
).groupBy(col("Flight_Delays")).agg(count("*").alias("total_delays")).orderBy(
    col("total_delays").desc()
).select(
    "total_delays", "Flight_Delays"
).show(
    10
)


# working with dataframes
