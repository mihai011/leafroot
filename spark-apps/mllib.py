from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, IntegerType, StructType
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


conf = SparkConf().setMaster("spark://spark:7077").setAppName("MLLib")
# conf = SparkConf().setMaster("local").setAppName("MovieRatings")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
spark.sparkContext.setLogLevel("WARN")

# reading parquet with data
filePath = """file:///opt/spark-data/sf-airbnb-clean.parquet"""
airbnbDF = spark.read.parquet(filePath)
airbnbDF.select(
    "neighbourhood_cleansed",
    "room_type",
    "bedrooms",
    "bathrooms",
    "number_of_reviews",
    "price",
).show(5)
airbnbDF.show(1)

feature_column = "review_scores_rating"
trainDF, testDF = airbnbDF.randomSplit([0.8, 0.2], seed=42)
print(
    f"""There are {trainDF.count()} rows in the training set,and {testDF.count()} in the test set"""
)

vecAssembler = VectorAssembler(inputCols=["bedrooms"], outputCol="features")
vecTrainDF = vecAssembler.transform(trainDF)
vecTestDF = vecAssembler.transform(testDF)
vecTrainDF.select(feature_column, "features", "price").show(10)

lr = LinearRegression(featuresCol="features", labelCol="price")
lrModel = lr.fit(vecTrainDF)

m = round(lrModel.coefficients[0], 2)
b = round(lrModel.intercept, 2)
print(
    f"""The formula for the linear regression line is price = {m}*{feature_column} + {b}"""
)

predictions = lrModel.transform(vecTestDF)

evaluator = RegressionEvaluator(
    labelCol=feature_column, predictionCol="price", metricName="rmse"
)
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) on test data: {:.3f}".format(rmse))

evaluator_r2 = RegressionEvaluator(
    labelCol=feature_column, predictionCol="price", metricName="r2"
)
r2 = evaluator_r2.evaluate(predictions)
print("R-squared (R2) on test data: {:.3f}".format(r2))

evaluator_r2 = RegressionEvaluator(
    labelCol=feature_column, predictionCol="price", metricName="mse"
)
r2 = evaluator_r2.evaluate(predictions)
print("Mean Squared Error (R2) on test data: {:.3f}".format(r2))
