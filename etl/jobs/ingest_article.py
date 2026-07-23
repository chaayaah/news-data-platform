from pyspark.sql import SparkSession

from etl.services.mapping_loader import MappingLoader
from etl.services.pipeline.context import PipelineContext
from etl.services.pipeline.factory import PipelineFactory
from etl.services.pipeline.stages import (
    PreGenericStage,
    VendorPreprocessorStage,
    ParserStage,
    PostGenericStage,
    ValidatorStage,
)
from etl.services.config import Config
from etl.services.validator import Validator

import json
import xml.etree.ElementTree as ET
import glob
import os

# -----------------------------
# Application Configuration
# -----------------------------

app_config = Config.load("app.json")

# -----------------------------
# Spark
# -----------------------------

spark = (
    SparkSession.builder
    .appName(app_config["spark"]["app_name"])
    .getOrCreate()
)

# -----------------------------
# Validation Rules
# -----------------------------

rules = Config.load("validation.json")
validator = Validator(rules)

# -----------------------------
# Pipeline Configuration
# -----------------------------

pipeline_config = Config.load("pipeline.json")

# -----------------------------
# Services
# -----------------------------

loader = MappingLoader()

# -----------------------------
# Pipeline Stages
# -----------------------------

stages = {
    "pre_generic": PreGenericStage(),
    "vendor_preprocessor": VendorPreprocessorStage(),
    "parser": ParserStage(),
    "post_generic": PostGenericStage(),
    "validator": ValidatorStage(validator),
}

pipeline = PipelineFactory.build_pipeline(
    pipeline_config["stages"],
    stages
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