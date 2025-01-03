
from functools import wraps
import time


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_tries=100):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal start_sleep_time
            for _ in range(max_tries):
                res = func(*args, **kwargs)
                if res:
                    break
                time.sleep(start_sleep_time)
                start_sleep_time = min(factor * start_sleep_time, border_sleep_time)
        return inner
    return func_wrapper