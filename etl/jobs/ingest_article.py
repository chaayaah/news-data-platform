from pyspark.sql import SparkSession
from etl.services.mapping_loader import MappingLoader
from etl.services.xml_parser import XMLParser
from etl.services.validator import Validator

import json
import xml.etree.ElementTree as ET
import glob
import os

# -----------------------------
# Spark
# -----------------------------

spark = SparkSession.builder \
    .appName("NewsDataPlatform") \
    .getOrCreate()

# -----------------------------
# Validation Rules
# -----------------------------

with open("/app/validation/rules.json") as f:
    rules = json.load(f)

required_fields = rules["required_fields"]

# -----------------------------
# Services
# -----------------------------

loader = MappingLoader()
parser = XMLParser()
validator = Validator(rules)

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

    records = parser.parse(
        root,
        mapping
    )

    print(f"Records Found: {len(records)}")

    for record in records:

        errors = validator.validate(record)

        if errors:

            invalid_records.append({
                "file": os.path.basename(xml_file),
                "errors": ", ".join(errors)
            })

            print(
                f"FAILED: {errors}"
            )

        else:

            valid_records.append(record)

            print(
                f"PASSED - {record['headline']}"
            )

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