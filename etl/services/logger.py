import logging
import os


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:
            return cls._logger

        os.makedirs("/app/logs", exist_ok=True)

        logger = logging.getLogger("NewsPipeline")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(message)s"
        )

        file_handler = logging.FileHandler(
            "/app/logs/pipeline.log"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger

        return logger