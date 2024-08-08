import time

from redis import Redis

from core.settings import settings

if __name__ == "__main__":
    r = Redis(host=settings.redis_host, port=settings.redis_port)
    while True:
        if r.ping():
            break
        time.sleep(1)
