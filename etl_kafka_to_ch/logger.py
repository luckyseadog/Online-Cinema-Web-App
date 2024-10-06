import logging
import sys

from configs.settings import settings


logger = settings.logger


def setup_logger() -> None:
    """Настройка логгирования для приложения и backoff"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)
    logger.setLevel(level=settings.log_level.upper())

    logging.getLogger("backoff").addHandler(logging.StreamHandler())
