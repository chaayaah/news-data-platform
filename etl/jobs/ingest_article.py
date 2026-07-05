from pyspark.sql import SparkSession
import json
import xml.etree.ElementTree as ET
import glob
import os

# Create Spark Session
spark = SparkSession.builder \
    .appName("NewsDataPlatform") \
    .getOrCreate()

# Load Vendor Registry
with open("/app/mappings/vendor_registry.json", "r") as f:
    vendor_registry = json.load(f)

# Load Validation Rules
with open("/app/validation/rules.json", "r") as f:
    rules = json.load(f)

required_fields = rules["required_fields"]

valid_records = []
invalid_records = []

# Loop through XML files
for xml_file in glob.glob("/app/sample_data/*.xml"):

    print(f"Processing: {os.path.basename(xml_file)}")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    publication = root.find("publication_name").text


    if publication not in vendor_registry:

        print(
            f"Unknown vendor: {publication}"
        )

        invalid_records.append({
            "file": os.path.basename(xml_file),
            "errors": f"Unknown vendor: {publication}"
        })

        continue

    mapping_filename = vendor_registry[publication]



    print(
        f"{os.path.basename(xml_file)} -> {mapping_filename}"
    )

    mapping_path = (
        f"/app/mappings/vendors/{mapping_filename}"
    )

    with open(mapping_path, "r") as f:
        mapping = json.load(f)

    record = {}

    # Apply Mapping
    for target_field, source_field in mapping.items():

        element = root.find(source_field)

        if element is not None:
            record[target_field] = element.text
        else:
            record[target_field] = None

    # Validation
    errors = []

    for field in required_fields:

        if not record.get(field):
            errors.append(f"{field} is missing")

    if errors:

        invalid_records.append({
            "file": os.path.basename(xml_file),
            "errors": ", ".join(errors)
        })

        print(f"FAILED: {errors}")

    else:

        valid_records.append(record)

        print("PASSED")

# Write Bronze
if valid_records:

    df = spark.createDataFrame(valid_records)

    print("\n=== VALID RECORDS ===")
    df.show(truncate=False)

    df.write.mode("overwrite").parquet(
        "/app/data/bronze/article"
    )

# Validation Summary
print("\n=== SUMMARY ===")
print(f"Valid Records: {len(valid_records)}")
print(f"Invalid Records: {len(invalid_records)}")

for invalid in invalid_records:
    print(invalid)

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

    print("Validation report saved")

spark.stop()