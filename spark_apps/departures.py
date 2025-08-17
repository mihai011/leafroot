"""This file contains example for sql queries and dataframe api.

All  are made on data from 'departures.csv' file.
"""

from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import col, count, when


def main() -> None:
    """Main function for reading csv file."""
    spark = SparkSession.builder.appName("SparkSQLExampleApp").getOrCreate()

    csv_file = "spark-data/departure_delays.csv"
    delay_360 = 360
    delay_150 = 150
    delay_120 = 120
    delay_60 = 60
    delay_0 = 0
    airport_sfo = "SFO"
    airport_ord = "ORD"
    distance = 1000

    # Read and create a temporary view
    # Infer schema (note that for larger files you
    # may want to specify the schema)
    df = (
        spark.read.format("csv")
        .option("inferSchema", "true")
        .option("header", "true")
        .load(csv_file)
    )
    spark.sparkContext.setLogLevel("WARN")
    df.createOrReplaceTempView("us_delay_flights_tbl")

    spark.sql(
        """
        SELECT distance, origin, destination FROM us_delay_flights_tbl
        WHERE distance > 1000 group by distance, origin, destination
        ORDER BY distance DESC
        """,
    ).show(5)

    df.select("distance", "origin", "destination").where(
        col("distance") > distance
    ).groupBy(
        col("distance"),
        col("origin"),
        col("destination"),
    ).count().drop(col("count")).orderBy(col("distance").desc()).show(5)

    spark.sql(
        """
        SELECT date, delay, origin, destination FROM us_delay_flights_tbl
        WHERE delay > 120 AND ORIGIN = 'SFO' AND DESTINATION = 'ORD' ORDER by delay DESC
        """,
    ).show(5)

    df.select("date", "delay", "origin", "destination").where(
        (col("delay") > delay_150)
        & (col("destination") == airport_ord)
        & (col("origin") == airport_sfo),
    ).orderBy(col("delay").desc()).show(5)

    spark.sql(
        """
        SELECT origin, destination, count(*) as delays FROM
        us_delay_flights_tbl group by origin, destination ORDER by delays DESC
        """,
    ).show(5)

    df.select("origin", "destination").groupBy(col("origin"), col("destination")).agg(
        count("*").alias("delays"),
    ).orderBy(col("delays").desc()).show(5)

    spark.sql(
        f"""SELECT count(*) as total_delays,
            CASE
            WHEN delay > {delay_360} THEN 'Very Long Delays'
            WHEN delay > {delay_120} AND delay < {delay_360} THEN 'Long Delays'
            WHEN delay > {delay_60} AND delay < {delay_120} THEN 'Short Delays'
            WHEN delay > {delay_0} and delay < {delay_60} THEN 'Tolerable Delays'
            WHEN delay = {delay_0} THEN 'No Delays' ELSE 'Early' END AS Flight_Delays
            FROM us_delay_flights_tbl
            group by Flight_Delays
            ORDER BY total_delays DESC""",
    ).show(10)

    df.withColumn(
        "Flight_Delays",
        when((col("delay") > delay_360), "Very Long Delays")
        .when((col("delay") > delay_120) & (col("delay") < delay_360), "Long Delays")
        .when((col("delay") > delay_60) & (col("delay") < delay_120), "Short Delays")
        .when((col("delay") > delay_0) & (col("delay") < delay_60), "Tolerable Delays")
        .when((col("delay") == 0), "No Delays")
        .otherwise("Early"),
    ).groupBy(col("Flight_Delays")).agg(count("*").alias("total_delays")).orderBy(
        col("total_delays").desc(),
    ).select("total_delays", "Flight_Delays").show(10)

    # working with dataframes writes
    # parquet
    df.write.format("parquet").mode("overwrite").option("compression", "snappy").save(
        "spark-data/dataframes_wr/departures.parquet",
    )

    df.write.mode("overwrite").parquet("spark-data/dataframes_wr/departures.parquet")

    df.write.format("json").mode("overwrite").option("compression", "snappy").save(
        "spark-data/dataframes_wr/",
    )
