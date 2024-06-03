import asyncio
import json
import logging

import aiohttp
from backoff import backoff

logging.basicConfig(level=logging.INFO)

class LoaderMovies:
    def __init__(self, host: str, port: int, index: str):
        self.host = host
        self.port = port
        self.index = index

    @backoff()
    async def start(self, lock, data):
        to_request = '\n'
        for key, value in data.items():
            to_request += json.dumps({'index': {'_index': self.index, '_id': key}}) + '\n'
            to_request += json.dumps(value) + '\n'

        await lock.acquire()
        try:
            headers = {'Content-Type': 'application/x-ndjson'}
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f'http://{self.host}:{self.port}/_bulk', 
                    headers=headers, 
                    data=to_request
                ) as resp:
                    resp.raise_for_status()
        finally:
            lock.release()

class LoaderPersons:
    def __init__(self, host: str, port: int, index: str):
        self.host = host
        self.port = port
        self.index = index

    @backoff()
    async def start(self, lock: asyncio.Lock, data) -> None:
        to_request = '\n'
        for key, value in data.items():
            to_request += json.dumps({'index': {'_index': self.index, '_id': key}}) + '\n'
            to_request += json.dumps(value) + '\n'

        await lock.acquire()
        try:
            headers = {'Content-Type': 'application/x-ndjson'}
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f'http://{self.host}:{self.port}/_bulk',
                    headers=headers,
                    data=to_request,
                ) as resp:
                    resp.raise_for_status()
        finally:
            lock.release()

class LoaderGenres:
    def __init__(self, host: str, port: int, index: str):
        self.host = host
        self.port = port
        self.index = index

    @backoff()
    async def start(self, lock, data):
        to_request = "\n"
        for key, value in data.items():
            to_request += json.dumps({"index": {"_index": self.index, "_id": key}}) + "\n"
            to_request += json.dumps(value) + "\n"

        await lock.acquire()
        try:
            headers = {'Content-Type': 'application/x-ndjson'}
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f'http://{self.host}:{self.port}/_bulk', 
                    headers=headers, 
                    data=to_request
                ) as resp:
                    resp.raise_for_status()
        finally:
            lock.release()

