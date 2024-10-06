import logging
import sys

from configs.settings import settings


def setup_logger() -> None:
    """Настройка логгирования для приложения и backoff"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
    settings.logger.addHandler(console_handler)
    settings.logger.setLevel(level=settings.log_level.upper())

    logging.getLogger("backoff").addHandler(logging.StreamHandler())
