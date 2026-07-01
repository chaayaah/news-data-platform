import subprocess

steps = [
    "pyspark/jobs/ingest_article.py",
    "pyspark/jobs/bronze_to_silver.py",
    "pyspark/jobs/silver_to_gold.py",
    "pyspark/jobs/gold_to_postgres.py"
]

print("=" * 60)
print("NEWS DATA PLATFORM PIPELINE")
print("=" * 60)

for step in steps:

    print(f"\nRunning: {step}")

    result = subprocess.run(
        ["python", step]
    )

    if result.returncode != 0:
        print(f"\nFAILED: {step}")
        exit(1)

    print(f"SUCCESS: {step}")

print("\nPipeline completed successfully.")