from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import backoff


@backoff(start_sleep_time=1, max_tries=3)
def ping_es(es_client):
    return es_client.ping()


if __name__ == '__main__':
    es_client = Elasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}', verify_certs=False)
    ping_es(es_client)
