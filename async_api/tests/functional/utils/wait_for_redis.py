from redis import Redis

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import backoff


@backoff(start_sleep_time=1, max_tries=3)
def ping_redis(redis_client):
    return redis_client.ping()

if __name__ == '__main__':
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    ping_redis(redis)