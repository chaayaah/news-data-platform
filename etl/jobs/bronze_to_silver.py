from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, trim
from orchestration.config import BRONZE_PATH

spark = SparkSession.builder \
    .appName("BronzeToSilver") \
    .getOrCreate()

# Read Bronze
bronze_df = spark.read.parquet(BRONZE_PATH)

print("\n=== BRONZE DATA ===")
bronze_df.show(truncate=False)

# Silver Transformations
silver_df = bronze_df \
    .withColumn(
        "publication_name",
        upper(trim(bronze_df.publication_name))
    ) \
    .withColumn(
        "author",
        upper(trim(bronze_df.author))
    ) \
    .withColumn(
        "headline",
        trim(bronze_df.headline)
    )

print("\n=== SILVER DATA ===")
silver_df.show(truncate=False)

# Write Silver Layer
silver_df.write.mode("overwrite").parquet(
    "/app/data/silver/article"
)

print("Silver layer saved")

spark.stop()