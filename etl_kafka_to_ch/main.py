from asyncio import get_event_loop
from contextlib import suppress
from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from clickhouse import init_clickhouse
from configs.settings import settings
from extractors import KafkaExtractor
from loaders import ClickhouseLoader
from logger import setup_logger


if TYPE_CHECKING:
    from models import Event


async def main() -> None:
    settings.logger.info("Старт etl")
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

    settings.logger.info("Etl завершен")


if __name__ == "__main__":
    setup_logger()
    init_clickhouse()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, "interval", seconds=settings.run_interval_seconds, max_instances=1)
    settings.logger.info("Запуск планировщика")
    scheduler.start()

    with suppress(KeyboardInterrupt, SystemExit):
        get_event_loop().run_forever()
