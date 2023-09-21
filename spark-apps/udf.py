"""Udf spark example.
"""

from pyspark.sql.types import LongType
import pandas as pd


def cubed(s):
    return s**3


from pyspark.sql import SparkSession  # Create a SparkSession
from pyspark.sql.functions import col, pandas_udf

spark = SparkSession.builder.appName("UDF").getOrCreate()
spark.udf.register("cubed", cubed, LongType())
spark.range(1, 9).createOrReplaceTempView("udf_test")
spark.sql("SELECT id, cubed(id) AS id_cubed FROM udf_test").show()

# Udf pandas dataframe

cubed_udf = pandas_udf(cubed, returnType=LongType())
x = pd.Series([1, 2, 3])
print(cubed(x))
df = spark.range(1, 4)
df.select("id", cubed_udf(col("id"))).show()
