import asyncio
import datetime
import logging
import os
import time
from datetime import timezone

from dotenv import load_dotenv
from es_loaders import LoaderGenres, LoaderMovies, LoaderPersons
from pg_extractors import ExtractorGenres, ExtractorMovies, ExtractorPersons
from redis import Redis
from setup import setup
from transformers import (
    TransformerGenres, TransformerMovies,
    TransformerPersons,
)

logging.basicConfig(level=logging.INFO)


async def ETL_process(process_name, redis_adapter, lock_postgres, lock_elastic, extructor, transformer, loader):
    TIME_DELTA = os.environ.get('TIME_DELTA')

    current_time = datetime.datetime.now().astimezone(datetime.timezone.utc)
    delta = datetime.timedelta(hours=int(TIME_DELTA))

    if redis_adapter.get(process_name) is None:
        redis_adapter.set(process_name, str(datetime.datetime(2024, 1, 1, tzinfo=timezone.utc)))

    while datetime.datetime.fromisoformat(redis_adapter.get(process_name)) < current_time:
        curr_delta = min(delta, current_time - datetime.datetime.fromisoformat(redis_adapter.get(process_name)))
        async for data in extructor.start(redis_adapter, lock_postgres, curr_delta):
            data = await transformer.start(data)
            await loader.start(lock_elastic, data)


async def main(dsn):
    lp_movies = asyncio.Lock()
    le_movies = asyncio.Lock()
    lp_genre = asyncio.Lock()
    le_genre = asyncio.Lock()
    lp_person = asyncio.Lock()
    le_person = asyncio.Lock()

    TIME_SYNC = os.environ.get('TIME_SYNC')
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
    ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

    redis_adapter = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    # TODO: make that data was loaded by different processes only once
    # NOTE: if you delete data in elastic - dont forget to delete progress in Redis

    while True:
        t1 = time.perf_counter()
        await asyncio.gather(
            *(
                ETL_process(process_name, redis_adapter, lp, le, ext, trm, ldr)
                for process_name, lp, le, ext, trm, ldr in [
                    (
                        'movies_genre',
                        lp_movies,
                        le_movies,
                        ExtractorMovies(dsn, proccess_name='movies_genre'),
                        TransformerMovies(),
                        LoaderMovies(host=ELASTIC_HOST, port=ELASTIC_PORT, index='movies'),
                    ),
                    (
                        'movies_film_work',
                        lp_movies,
                        le_movies,
                        ExtractorMovies(dsn, proccess_name='movies_film_work'),
                        TransformerMovies(),
                        LoaderMovies(host=ELASTIC_HOST, port=ELASTIC_PORT, index='movies'),
                    ),
                    (
                        'movies_person',
                        lp_movies,
                        le_movies,
                        ExtractorMovies(dsn, proccess_name='movies_person'),
                        TransformerMovies(),
                        LoaderMovies(host=ELASTIC_HOST, port=ELASTIC_PORT, index='movies'),
                    ),
                    (
                        'genre',
                        lp_genre,
                        le_genre,
                        ExtractorGenres(dsn, proccess_name='genre'),
                        TransformerGenres(),
                        LoaderGenres(host=ELASTIC_HOST, port=ELASTIC_PORT, index='genres'),
                    ),
                    (
                        'person',
                        lp_person,
                        le_person,
                        ExtractorPersons(dsn, proccess_name='person'),
                        TransformerPersons(),
                        LoaderPersons(host=ELASTIC_HOST, port=ELASTIC_PORT, index='persons'),
                    ),
                ]
            ),
        )

        redis_adapter.bgsave()
        logging.info(f'TIME: {time.perf_counter() - t1} s')
        await asyncio.sleep(int(TIME_SYNC))


if __name__ == '__main__':
    load_dotenv()

    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('HOST')
    DB_PORT = int(os.environ.get('PORT', 5432))
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
    ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

    for index, file in (
        ('movies', 'es_config/movies.json'),
        ('persons', 'es_config/persons.json'),
        ('genres', 'es_config/genres.json'),
    ):
        setup(ELASTIC_HOST, ELASTIC_PORT, index, file)

    dsn = {'dbname': DB_NAME, 'user': DB_USER, 'password': DB_PASSWORD, 'host': DB_HOST, 'port': DB_PORT}

    asyncio.run(main(dsn))
