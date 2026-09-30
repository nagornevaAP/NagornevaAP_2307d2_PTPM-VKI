import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "file_txt.log")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
    )
    logging.info("Логгер успешно сконфигурирован")

