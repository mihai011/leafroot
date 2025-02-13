"""Just a file for pyspark test"""

from pyspark.sql import SparkSession  # Create a SparkSession

spark = (
    SparkSession.builder.remote("sc://spark")
    .config("spark.network.timeout", "5s")
    .config("spark.executor.heartbeatInterval", "5s")
    .getOrCreate()
)

data = [
    ("James", "", "Smith", "1991-04-01", "M", 3000),
    ("Michael", "Rose", "", "2000-05-19", "M", 4000),
    ("Robert", "", "Williams", "1978-09-05", "M", 4000),
    ("Maria", "Anne", "Jones", "1967-12-01", "F", 4000),
    ("Jen", "Mary", "Brown", "1980-02-17", "F", -1),
]

columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]
df = spark.createDataFrame(data=data, schema=columns)
df.show()
