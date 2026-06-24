from pyspark.sql import SparkSession
import json
import xml.etree.ElementTree as ET

# Create Spark Session
spark = SparkSession.builder \
    .appName("NewsDataPlatform") \
    .getOrCreate()

# Read XML
tree = ET.parse("/app/sample_data/article.xml")
root = tree.getroot()


# Read Mapping
with open("/app/mappings/article_mapping.json", "r") as f:
    mapping = json.load(f)

# Transform XML -> Dictionary
record = {}

for target_field, source_field in mapping.items():

    element = root.find(source_field)

    if element is not None:
        record[target_field] = element.text
    else:
        record[target_field] = None

# Debug Output
print("\n=== RECORD ===")
print(record)

# Create DataFrame
df = spark.createDataFrame([record])

print("\n=== ARTICLE DATA ===")
df.show(truncate=False)

# Write to Bronze Layer
df.write.mode("overwrite").parquet(
    "/app/data/bronze/article"
)

print("Saved to Bronze Layer")

spark.stop()