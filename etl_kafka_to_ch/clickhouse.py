import backoff
from clickhouse_connect import get_client
from clickhouse_connect.driver.exceptions import OperationalError

from configs.settings import settings


@backoff.on_exception(backoff.expo, OperationalError, max_tries=10, max_time=10)
def init_clickhouse() -> None:
    client = get_client(
        host=settings.ch_host,
        username=settings.ch_user,
        password=settings.ch_password,
    )
    settings.logger.info("Инициализация clickhouse")

    result = client.command(f"CREATE DATABASE IF NOT EXISTS {settings.ch_database} ON CLUSTER company_cluster")
    settings.logger.info(f"Создали базу данных  '{settings.ch_database}'. Результат: {result}")

    result = client.command(
        f"CREATE TABLE IF NOT EXISTS {settings.ch_database}.{settings.ch_table} ON CLUSTER company_cluster "
        "(...) Engine=MergeTree() ORDER BY timestamp"  # TODO: описать таблицу
    )
    settings.logger.info(f"Создали таблицу '{settings.ch_table}'. Результат: {result}")
