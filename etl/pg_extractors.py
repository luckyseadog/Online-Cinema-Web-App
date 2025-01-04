import datetime
import logging

import psycopg
from backoff import backoff_generator
from sql_queries import (
    EXTRUCT, FILM_IDS_BY_GENRE, FILM_IDS_BY_PERSON,
    RAW_GENRE_EXTRUCT, RAW_PERSONS, WHERE_CLAUSE_IN,
    WHERE_CLAUSE_MODIFIED,
)

logging.basicConfig(level=logging.INFO)


class ExtractorMovies:
    def __init__(self, dsn, proccess_name, fetch_size=100):
        self.dsn = dsn
        self.proccess_name = proccess_name
        self.fetch_size = fetch_size

    async def _extruct_filmwork(self, acur, from_time, till_time):
        where_clause = WHERE_CLAUSE_MODIFIED % (str(from_time), str(till_time))
        await acur.execute(EXTRUCT.format(where_clause))
        while res := await acur.fetchmany(self.fetch_size):
            yield res

    async def _extruct_genre(self, acur, from_time, till_time):
        await acur.execute(FILM_IDS_BY_GENRE, (str(from_time), str(till_time)))
        res = await acur.fetchall()
        flat_res = ["'" + str(item) + "'" for sublist in res for item in sublist]
        if len(flat_res) > 0:
            where_clause = WHERE_CLAUSE_IN.format(', '.join(flat_res))
            await acur.execute(EXTRUCT.format(where_clause))
            while res := await acur.fetchmany(self.fetch_size):
                yield res

    async def _extruct_person(self, acur, from_time, till_time):
        await acur.execute(FILM_IDS_BY_PERSON, (str(from_time), str(till_time)))
        res = await acur.fetchall()
        flat_res = ["'" + str(item) + "'" for sublist in res for item in sublist]
        if len(flat_res) > 0:
            where_clause = WHERE_CLAUSE_IN.format(', '.join(flat_res))
            await acur.execute(EXTRUCT.format(where_clause))
            while res := await acur.fetchmany(self.fetch_size):
                yield res

    @backoff_generator()
    async def start(self, redis_adapter, lock, time_delta):
        from_time = datetime.datetime.fromisoformat(redis_adapter.get(self.proccess_name))
        till_time = from_time + time_delta
        await lock.acquire()
        try:
            async with await psycopg.AsyncConnection.connect(**self.dsn) as aconn:
                async with aconn.cursor() as acur:
                    if self.proccess_name == 'movies_film_work':
                        async for res in self._extruct_filmwork(acur, from_time, till_time):
                            yield res
                    elif self.proccess_name == 'movies_genre':
                        async for res in self._extruct_genre(acur, from_time, till_time):
                            yield res
                    elif self.proccess_name == 'movies_person':
                        async for res in self._extruct_person(acur, from_time, till_time):
                            yield res
            redis_adapter.set(self.proccess_name, str(till_time))
        finally:
            if self.proccess_name == 'movies_genre':
                logging.info(f'GENRE: {redis_adapter.get(self.proccess_name)}')
            lock.release()

class ExtractorPersons:
    def __init__(self, dsn: dict, proccess_name: str):
        self.dsn = dsn
        self.proccess_name = proccess_name

    @backoff_generator()
    async def start(self, redis_adapter, lock, time_delta, fetch_size=100):
        from_time = datetime.datetime.fromisoformat(redis_adapter.get(self.proccess_name))
        till_time = from_time + time_delta
        await lock.acquire()
        try:
            async with await psycopg.AsyncConnection.connect(**self.dsn) as aconn:
                async with aconn.cursor() as acur:
                    await acur.execute(RAW_PERSONS, (str(from_time), str(till_time)))
                    while res := await acur.fetchmany(fetch_size):
                        yield res
            redis_adapter.set(self.proccess_name, str(till_time))
        finally:
            lock.release()

class ExtractorGenres:
    def __init__(self, dsn, proccess_name):
        self.dsn = dsn
        self.proccess_name = proccess_name

    @backoff_generator()
    async def start(self, redis_adapter, lock, time_delta, fetch_size=100):
        from_time = datetime.datetime.fromisoformat(redis_adapter.get(self.proccess_name))
        till_time = from_time + time_delta
        await lock.acquire()
        try:
            async with await psycopg.AsyncConnection.connect(**self.dsn) as aconn:
                async with aconn.cursor() as acur:
                    await acur.execute(RAW_GENRE_EXTRUCT, (str(from_time), str(till_time)))
                    while res := await acur.fetchmany(fetch_size):
                        yield res
            redis_adapter.set(self.proccess_name, str(till_time))
        finally:
            lock.release()
