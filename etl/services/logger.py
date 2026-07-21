import logging
import os

from etl.services.config import Config


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:
            return cls._logger

        config = Config.load("logging.json")
        logging_config = config["logging"]

        os.makedirs("/app/logs", exist_ok=True)

        logger = logging.getLogger("NewsPipeline")

        logger.setLevel(
            getattr(logging, logging_config["level"].upper())
        )

        formatter = logging.Formatter(
            logging_config["format"]
        )

        file_handler = logging.FileHandler(
            logging_config["file"]
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Prevent duplicate handlers if logger is recreated
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._logger = logger

        return logger