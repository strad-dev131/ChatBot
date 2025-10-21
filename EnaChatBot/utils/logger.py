import logging
import os

DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with consistent formatting and level.
    Respects LOG_LEVEL environment variable (default INFO).
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(format=DEFAULT_FORMAT, level=level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger