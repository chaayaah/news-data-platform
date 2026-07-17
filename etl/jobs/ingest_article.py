from pyspark.sql import SparkSession

from etl.services.mapping_loader import MappingLoader
from etl.services.pipeline.context import PipelineContext
from etl.services.pipeline.factory import PipelineFactory

import json
import xml.etree.ElementTree as ET
import glob
import os

# -----------------------------
# Spark
# -----------------------------

spark = (
    SparkSession.builder
    .appName("NewsDataPlatform")
    .getOrCreate()
)

# -----------------------------
# Validation Rules
# -----------------------------

with open("/app/validation/rules.json") as f:
    rules = json.load(f)

# -----------------------------
# Pipeline Configuration
# -----------------------------

with open("/app/config/pipeline.json") as f:
    pipeline_config = json.load(f)

# -----------------------------
# Services
# -----------------------------

loader = MappingLoader()

pipeline = PipelineFactory.build_pipeline(
    pipeline_config["stages"],
    rules
)

valid_records = []
invalid_records = []

# -----------------------------
# Process XML Files
# -----------------------------

for xml_file in glob.glob("/app/sample_data/*/raw/*.xml"):

    print("=" * 60)
    print(f"Processing: {xml_file}")

    vendor = os.path.basename(
        os.path.dirname(
            os.path.dirname(xml_file)
        )
    )

    print(f"Vendor: {vendor}")

    try:

        mapping = loader.load_mapping(vendor)

    except ValueError as e:

        print(e)

        invalid_records.append({
            "file": os.path.basename(xml_file),
            "errors": str(e)
        })

        continue

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # -----------------------------
    # Create Pipeline Context
    # -----------------------------

    context = PipelineContext()

    context.vendor = vendor
    context.mapping = mapping
    context.root = root

    # -----------------------------
    # Run Pipeline
    # -----------------------------

    context = pipeline.run(context)

    print(f"Records Found: {len(context.records)}")

    valid_records.extend(context.valid_records)

    for invalid in context.invalid_records:

        invalid_records.append({
            "file": os.path.basename(xml_file),
            "errors": ", ".join(invalid["errors"])
        })

    for record in context.valid_records:

        print(f"PASSED - {record['headline']}")

    for invalid in context.invalid_records:

        print(f"FAILED - {', '.join(invalid['errors'])}")

# -----------------------------
# Write Bronze
# -----------------------------

if valid_records:

    df = spark.createDataFrame(valid_records)

    print("\n=== BRONZE DATA ===")

    df.show(truncate=False)

    df.write.mode("overwrite").parquet(
        "/app/data/bronze/article"
    )

# -----------------------------
# Summary
# -----------------------------

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Valid Records: {len(valid_records)}")
print(f"Invalid Records: {len(invalid_records)}")

for invalid in invalid_records:
    print(invalid)

# -----------------------------
# Reject Report
# -----------------------------

if invalid_records:

    with open(
        "/app/data/rejects/validation_report.json",
        "w"
    ) as f:

        json.dump(
            invalid_records,
            f,
            indent=4
        )

spark.stop()