from pyspark.sql import SparkSession
from etl.services.mapping_loader import MappingLoader

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
# Services
# -----------------------------

loader = MappingLoader()

# -----------------------------
# Validation Rules
# -----------------------------

with open("/app/validation/rules.json") as f:
    rules = json.load(f)

required_fields = rules["required_fields"]

valid_records = []
invalid_records = []

# -----------------------------
# Process every vendor XML
# -----------------------------

for xml_file in glob.glob("/app/sample_data/*/raw/*.xml"):

    print("=" * 60)
    print(f"Processing: {xml_file}")

    # Vendor comes from folder name
    # sample_data/Reuters/raw/file.xml
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

    record_tag = mapping["record_tag"]

    records = root.findall(record_tag)

    print(f"Records Found: {len(records)}")

    # -----------------------------
    # Process every document
    # -----------------------------

    for record in records:

        normalized = {}

        for target_field, source_field in mapping.items():

            if target_field == "record_tag":
                continue

            element = record.find(source_field)

            if element is not None:

                normalized[target_field] = (
                    element.text.strip()
                    if element.text
                    else ""
                )

            else:

                normalized[target_field] = None

        # -------------------------
        # Validation
        # -------------------------

        errors = []

        for field in required_fields:

            if not normalized.get(field):

                errors.append(
                    f"{field} is missing"
                )

        if errors:

            invalid_records.append({
                "file": os.path.basename(xml_file),
                "errors": ", ".join(errors)
            })

            print(
                f"FAILED: {errors}"
            )

        else:

            valid_records.append(
                normalized
            )

            print(
                f"PASSED - {normalized['headline']}"
            )

# -----------------------------
# Write Bronze
# -----------------------------

if valid_records:

    df = spark.createDataFrame(
        valid_records
    )

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

print(
    f"Valid Records: {len(valid_records)}"
)

print(
    f"Invalid Records: {len(invalid_records)}"
)

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