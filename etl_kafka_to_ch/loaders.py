import backoff
from clickhouse_connect import get_client
from clickhouse_connect.driver.exceptions import Error, OperationalError

from configs.settings import settings
from models import Event


logger = settings.logger


class ClickhouseLoader:
    def __init__(self) -> None:
        self.get_client_clickhouse()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=10, max_time=10)
    def get_client_clickhouse(self) -> None:
        self.client = get_client(
            host=settings.ch_host,
            database=settings.ch_database,
            username=settings.ch_user,
            password=settings.ch_password,
        )

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=10, max_time=10)
    def load_batch(self, event_batch: list[Event]) -> None:
        if not event_batch:
            return

        data = tuple(tuple(event.model_dump().values()) for event in event_batch)
        try:
            result = self.client.insert(table=settings.ch_table, data=data, column_names=Event.model_fields.keys())
        except Error:
            logger.exception(f"Ошибка при загрузке пакета в clickhouse {data}")
        else:
            logger.info(f"Загруженная партия {event_batch} с результатом {result.summary}")
