"""Expr utility example."""

from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import expr


def main() -> None:
    """Main function for file reading."""
    spark = SparkSession.builder.appName("UDF").getOrCreate()

    trip_delays_file_path = "spark-data/departure_delays.csv"
    airports_na_file_path = "spark-data/airport-codes-na.txt"

    airports_na = (
        spark.read.format("csv")
        .options(header="true", inferSchema=True, sep="\t")
        .load(airports_na_file_path)
    )

    airports_na.createOrReplaceTempView("airports_na")

    departure_delays = (
        spark.read.format("csv")
        .options(header="true", inferSchema=True)
        .load(trip_delays_file_path)
    )

    departure_delays = departure_delays.withColumn(
        "delay",
        expr("CAST(delay as INT) as delay"),
    ).withColumn("distance", expr("CAST(distance as INT) as distance"))

    departure_delays.createOrReplaceTempView("departure_delays")

    foo = departure_delays.filter(expr("""origin == 'SEA' and destination == 'SFO'"""))
    foo.createOrReplaceTempView("foo")

    spark.sql("select * from airports_na limit 10").show()
    spark.sql("select * from  departure_delays limit 10").show()
    spark.sql("select * from  foo").show()

    # union
    bar = departure_delays.union(foo)
    bar.createOrReplaceTempView("bar")

    spark.sql(
        """
        SELECT * FROM bar WHERE
        origin = 'SEA' AND destination = 'SFO' AND date LIKE '01010%' AND delay > 0
        """,
    ).show()
