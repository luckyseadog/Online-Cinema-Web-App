import time

from redis import Redis

from core.settings import test_settings


if __name__ == "__main__":
    r = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    while True:
        if r.ping():
            break
        time.sleep(1)
