"""Just file for spark experimentation."""

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import count

if __name__ == "__main__":
    exp_args = 2
    if len(sys.argv) != exp_args:
        print("Usage: mmcounter <file>", file=sys.stderr)
        sys.exit(-1)

    spark = (
        SparkSession.builder.appName("pythonmmcount")
        .master("spark://spark:7077")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    mnm_file = sys.argv[1]
    mnm_df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(mnm_file)
    )
    count_mnm_df = (
        mnm_df.select("State", "Color", "Count")
        .groupBy("State", "Color")
        .agg(count("Count").alias("Total"))
        .orderBy("Total", ascending=False)
    )
    count_mnm_df.show(n=50, truncate=False)
    print(f"Total Rows = {count_mnm_df.count()}")
    ca_count_mnm_df = (
        mnm_df.select("State", "Color", "Count")
        .where(mnm_df.State == "CA")
        .groupBy("State", "Color")
        .agg(count("Count").alias("Total"))
        .orderBy("Total", ascending=False)
    )
    ca_count_mnm_df.show(n=10, truncate=False)
    spark.stop()
