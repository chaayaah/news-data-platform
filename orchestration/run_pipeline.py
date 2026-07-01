import subprocess
import time

from orchestration.logger import logger
from orchestration.db import (
    start_pipeline,
    finish_pipeline,
    fail_pipeline
)


steps = [
    "pyspark/jobs/ingest_article.py",
    "pyspark/jobs/bronze_to_silver.py",
    "pyspark/jobs/silver_to_gold.py",
    "pyspark/jobs/gold_to_postgres.py"
]


def log(message):
    print(message)
    logger.info(message)


log("=" * 60)
log("NEWS DATA PLATFORM PIPELINE")
log("=" * 60)

start = time.time()

pipeline_id = start_pipeline("News Data Pipeline")

log(f"Pipeline ID: {pipeline_id}")

for step in steps:

    log(f"\nRunning: {step}")

    result = subprocess.run(
        ["python", step]
    )

    if result.returncode != 0:

        duration = int(time.time() - start)

        fail_pipeline(
            pipeline_id,
            duration,
            f"{step} failed"
        )

        logger.error(f"FAILED: {step}")

        print(f"\nFAILED: {step}")

        exit(1)

    log(f"SUCCESS: {step}")

duration = int(time.time() - start)

# TODO:
# Read this dynamically from the pipeline
records_processed = 3

finish_pipeline(
    pipeline_id,
    duration,
    records_processed
)

log("\nPipeline completed successfully.")