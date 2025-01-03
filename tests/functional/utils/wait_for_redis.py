import backoff
from redis import ConnectionError, Redis

from core.settings import test_settings


@backoff.on_exception(backoff.expo, ConnectionError, max_tries=10)
def wait_for_redis(redis_client: Redis):
    if not redis_client.ping():
        raise ConnectionError("Elasticsearch is not running.")


if __name__ == "__main__":
    redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    wait_for_redis(redis_client)
