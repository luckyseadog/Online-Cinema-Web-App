"""
This type stub file was generated by pyright.
"""

import asyncio
from asyncio import AbstractEventLoop
from typing import Any, TypeVar
from collections.abc import Awaitable, Coroutine
from .structs import OffsetAndMetadata, TopicPartition

__all__ = ["INTEGER_MAX_VALUE", "INTEGER_MIN_VALUE", "NO_EXTENSIONS", "create_future", "create_task"]
T = TypeVar("T")

def create_task(coro: Coroutine[Any, Any, T]) -> asyncio.Task[T]: ...
def create_future(loop: AbstractEventLoop | None = ...) -> asyncio.Future[T]: ...
async def wait_for(fut: Awaitable[T], timeout: None | int | float = ...) -> T: ...
def parse_kafka_version(api_version: str) -> tuple[int, int, int]: ...
def commit_structure_validate(
    offsets: dict[TopicPartition, int | tuple[int, str] | OffsetAndMetadata],
) -> dict[TopicPartition, OffsetAndMetadata]: ...
def get_running_loop() -> asyncio.AbstractEventLoop: ...

NO_EXTENSIONS = ...
INTEGER_MAX_VALUE = ...
INTEGER_MIN_VALUE = ...
