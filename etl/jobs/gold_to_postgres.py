from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from orchestration.config import GOLD_PATH

spark = SparkSession.builder \
    .appName("GoldToPostgres") \
    .config(
        "spark.jars",
        "/opt/jars/postgresql.jar"
    ) \
    .getOrCreate()

# Read Gold Layer
gold_df = spark.read.parquet(GOLD_PATH)
print("\n=== GOLD DATA ===")
gold_df.show(truncate=False)

# Rename count column to match PostgreSQL table
gold_df = gold_df.withColumnRenamed(
    "count",
    "article_count"
)

print("\n=== DATA TO LOAD ===")
gold_df.show(truncate=False)

# Write to PostgreSQL
gold_df.write \
    .format("jdbc") \
    .option(
        "url",
        "jdbc:postgresql://news-postgres:5432/newsdb"
    ) \
    .option(
        "dbtable",
        "article_summary"
    ) \
    .option(
        "user",
        "postgres"
    ) \
    .option(
        "password",
        "postgres"
    ) \
    .option(
        "driver",
        "org.postgresql.Driver"
    ) \
    .mode("overwrite") \
    .save()

print("Loaded Gold Layer to PostgreSQL")

spark.stop()