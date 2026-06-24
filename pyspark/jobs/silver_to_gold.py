from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SilverToGold") \
    .getOrCreate()

# Read Silver
silver_df = spark.read.parquet(
    "/app/data/silver/article"
)

print("\n=== SILVER DATA ===")
silver_df.show(truncate=False)

# Gold Aggregation
gold_df = silver_df.groupBy("country").count()

print("\n=== GOLD DATA ===")
gold_df.show(truncate=False)

# Write Gold Layer
gold_df.write.mode("overwrite").parquet(
    "/app/data/gold/article_summary"
)

print("Gold layer saved")

spark.stop()