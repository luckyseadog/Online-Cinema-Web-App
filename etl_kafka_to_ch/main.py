from asyncio import get_event_loop
from contextlib import suppress
from typing import TYPE_CHECKING

import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from clickhouse import init_clickhouse
from configs.settings import settings
from extractors import KafkaExtractor
from loaders import ClickhouseLoader
from logger import setup_logger


if TYPE_CHECKING:
    from models import Event

logger = settings.logger


if settings.sentry_on:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


async def main() -> None:
    logger.info("Старт etl")
    loader = ClickhouseLoader()
    batches: list[Event] = []
    async with KafkaExtractor() as extractor:
        async for item in extractor.extract():
            if item is not None:
                batches.append(item)
                if len(batches) == settings.batch_size:
                    loader.load_batch(batches)
                    batches = []

        loader.load_batch(batches)

    logger.info("Etl завершен")


if __name__ == "__main__":
    setup_logger()
    init_clickhouse()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, "interval", seconds=settings.run_interval_seconds, max_instances=1)
    logger.info("Запуск планировщика")
    scheduler.start()

    with suppress(KeyboardInterrupt, SystemExit):
        get_event_loop().run_forever()
