"""Module for spark vectors."""

from pyspark import SparkConf, SparkContext
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession


def main() -> None:
    """Main function for the set."""
    conf = SparkConf().setMaster("spark://spark:7077").setAppName("MLLib")
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)
    spark.sparkContext.setLogLevel("WARN")

    # reading parquet with data
    file_path = """file:///opt/spark-data/sf-airbnb-clean.parquet"""
    airbnb_df = spark.read.parquet(file_path)
    airbnb_df.select(
        "neighbourhood_cleansed",
        "room_type",
        "bedrooms",
        "bathrooms",
        "number_of_reviews",
        "price",
    ).show(5)
    airbnb_df.show(1)

    feature_column = "review_scores_rating"
    train_df, test_df = airbnb_df.randomSplit([0.8, 0.2], seed=42)
    print(
        f"""There are {train_df.count()} rows in the training set,\
            and {test_df.count()} in the test set""",
    )

    ve_assembler = VectorAssembler(inputCols=["bedrooms"], outputCol="features")
    ve_train_df = ve_assembler.transform(train_df)
    ve_train_df = ve_assembler.transform(test_df)
    ve_train_df.select(feature_column, "features", "price").show(10)

    lr = LinearRegression(featuresCol="features", labelCol="price")
    lr_model = lr.fit(ve_train_df)

    m = round(lr_model.coefficients[0], 2)
    b = round(lr_model.intercept, 2)
    print(
        f"""The formula for the linear regression line is price \
            = {m}*{feature_column} + {b}""",
    )

    predictions = lr_model.transform(ve_train_df)

    evaluator = RegressionEvaluator(
        labelCol=feature_column,
        predictionCol="price",
        metricName="rmse",
    )
    rmse = evaluator.evaluate(predictions)
    print(f"Root Mean Squared Error (RMSE) on test data: {rmse:.3f}")

    evaluator_r2 = RegressionEvaluator(
        labelCol=feature_column,
        predictionCol="price",
        metricName="r2",
    )
    r2 = evaluator_r2.evaluate(predictions)
    print(f"R-squared (R2) on test data: {r2:.3f}")

    evaluator_r2 = RegressionEvaluator(
        labelCol=feature_column,
        predictionCol="price",
        metricName="mse",
    )
    r2 = evaluator_r2.evaluate(predictions)
    print(f"Mean Squared Error (R2) on test data: {r2:.3f}")
