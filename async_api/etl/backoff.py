import asyncio
import logging
from functools import wraps

import aiohttp
import psycopg

logging.basicConfig(level=logging.INFO)


def backoff_generator(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_tries=100):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal start_sleep_time
            for _ in range(max_tries):
                try:
                    async for res in func(*args, **kwargs):
                        logging.info(f"Rows changed: {len(res)}")
                        yield res
                    return
                except psycopg.DatabaseError:
                    await asyncio.sleep(start_sleep_time)
                    start_sleep_time = min(factor * start_sleep_time, border_sleep_time)
                except Exception as e:
                    logging.warn("Error with data syncronization: some data is not loaded in Elastic", e)
        return inner
    return func_wrapper


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_tries=100):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal start_sleep_time
            for _ in range(max_tries):
                try:
                    await func(*args, **kwargs)
                    return
                except aiohttp.ClientResponseError:
                    await asyncio.sleep(start_sleep_time)
                    start_sleep_time = min(factor * start_sleep_time, border_sleep_time)
                except Exception as e:
                    logging.warn("Error with data syncronization: some data is not loaded in Elastic", e)
                    return
        return inner
    return func_wrapper
