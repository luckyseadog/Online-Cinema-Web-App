import time

from elasticsearch import Elasticsearch

from core.settings import settings

if __name__ == "__main__":
    es_client = Elasticsearch(hosts=settings.elastic_dsn)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
