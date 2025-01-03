from typing import Any

import backoff
import psycopg

from core.settings import test_settings


@backoff.on_exception(backoff.expo, psycopg.OperationalError, max_tries=10)
def wait_for_postgres(cursor: psycopg.Cursor[Any]) -> None:
    cursor.execute("SELECT 1")


if __name__ == "main":
    with psycopg.connect(**test_settings.postgres_dsn) as conn, conn.cursor() as cursor:
        wait_for_postgres(cursor)
