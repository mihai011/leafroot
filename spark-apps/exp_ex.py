"""
Expr utility example
"""

from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder.appName("UDF").getOrCreate()

tripDelaysFilePath = "spark-data/departuredelays.csv"
airportsnaFilePath = "spark-data/airport-codes-na.txt"

airportsna = (
    spark.read.format("csv")
    .options(header="true", inferSchema=True, sep="\t")
    .load(airportsnaFilePath)
)

airportsna.createOrReplaceTempView("airports_na")

departureDelays = (
    spark.read.format("csv")
    .options(header="true", inferSchema=True)
    .load(tripDelaysFilePath)
)

departureDelays = departureDelays.withColumn(
    "delay", expr("CAST(delay as INT) as delay")
).withColumn("distance", expr("CAST(distance as INT) as distance"))

departureDelays.createOrReplaceTempView("departureDelays")

foo = departureDelays.filter(expr("""origin == 'SEA' and destination == 'SFO'"""))
foo.createOrReplaceTempView("foo")

spark.sql("select * from airports_na limit 10").show()
spark.sql("select * from  departureDelays limit 10").show()
spark.sql("select * from  foo").show()

# union
bar = departureDelays.union(foo)
bar.createOrReplaceTempView("bar")

spark.sql(
    """ SELECT * FROM bar WHERE origin = 'SEA' AND destination = 'SFO' AND date LIKE '01010%' AND delay > 0 """
).show()
