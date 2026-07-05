import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

BRONZE_PATH = os.getenv("BRONZE_PATH")
SILVER_PATH = os.getenv("SILVER_PATH")
GOLD_PATH = os.getenv("GOLD_PATH")

PIPELINE_NAME = os.getenv("PIPELINE_NAME")