"""Postgress import source."""

from pyspark.sql import SparkSession  # Create a SparkSession

spark = SparkSession.builder.appName("Postgress app").getOrCreate()


def main() -> None:
    """Postgres spark example."""
    jdbc_df1 = (
        spark.read.format("jdbc")
        .option("url", "jdbc:postgresql://db/app")
        .option("dbtable", "public.users")
        .option("user", "postgres")
        .option("password", "pass")
        .load()
    )

    jdbc_df1.show()
