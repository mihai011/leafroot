from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from pyspark.sql.window import Window

conf = SparkConf().setMaster("spark://spark:7077").setAppName("Example")
# conf = SparkConf().setMaster("local").setAppName("MovieRatings")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
spark.sparkContext.setLogLevel("WARN")


# Define the structure for the data frame
department_schema = StructType(
    [
        StructField("Department_ID", IntegerType(), True),
        StructField("Department_Name", StringType(), True),
    ]
)

person_schema = StructType(
    [
        StructField("Badge_ID", IntegerType(), True),
        StructField("Person_Name", StringType(), True),
        StructField("Department_ID", IntegerType(), True),
        StructField("Salary", IntegerType(), True),
    ]
)


# reading directly into a DataFrame with SparSession, but could be json, parquet, text etc.
department_df = spark.read.csv(
    "file:///opt/spark-data/department.csv",
    header=True,
    schema=department_schema,
)
person_df = spark.read.csv(
    "file:///opt/spark-data/person.csv", header=True, schema=person_schema
)

print(department_df.show())
print(department_df.printSchema())

print(person_df.show())
print(person_df.printSchema())

# Average Salary per Department
joined_df = person_df.groupBy(person_df.Department_ID).agg({"Salary": "avg"})
print(joined_df.show())
print(joined_df.printSchema())

# Highest Salary per Department
joined_df = person_df.groupBy(person_df.Department_ID).agg({"Salary": "max"})
print(joined_df.show())
print(joined_df.printSchema())

# Get number of Employees on each Department
joined_df = person_df.groupBy(person_df.Department_ID).count()
print(joined_df.show())
print(joined_df.printSchema())

# Select person on each Department with the highest salary
windowDept = Window.partitionBy("Department_Name").orderBy(col("Salary").desc())
joined_df = (
    person_df.join(department_df, "Department_ID")
    .select(["Department_Name", "Person_Name", "Salary"])
    .withColumn("position_in_department", row_number().over(windowDept))
    .filter(col("position_in_department") == 1)
    .drop("position_in_department")
)
print(joined_df.show())
print(joined_df.printSchema())

# Select person on each Department with the highest salary with sql syntax
person_df.createOrReplaceTempView("Person")
department_df.createOrReplaceTempView("Department")
joined_df = spark.sql(
    """
            select Person_Name, Department_name, Salary from
            (select *,
            row_number() OVER (PARTITION BY Department_Name ORDER BY salary DESC) as position_in_department
            from Person p join Department d on d.Department_ID = p.Department_ID) where position_in_department = 1"""
)
print(joined_df.show())
print(joined_df.printSchema())
