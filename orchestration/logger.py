import logging

logging.basicConfig(
    filename="/app/logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("pipeline")