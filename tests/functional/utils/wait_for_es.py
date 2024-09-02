import backoff
from elasticsearch import ConnectionError, Elasticsearch

from core.settings import test_settings


@backoff.on_exception(backoff.expo, ConnectionError, max_tries=10)
def wait_for_es(es_client: Elasticsearch) -> None:
    if not es_client.ping():
        raise ConnectionError("Elasticsearch is not running.")


if __name__ == "__main__":
    es_client = Elasticsearch(hosts=test_settings.elastic_dsn)
    wait_for_es(es_client)
