"""
This type stub file was generated by pyright.
"""

from typing import final
from aiokafka.util import NO_EXTENSIONS
from ._protocols import DefaultRecordBatchProtocol, LegacyRecordBatchProtocol, MemoryRecordsProtocol

@final
class _MemoryRecordsPy(MemoryRecordsProtocol):
    LENGTH_OFFSET = ...
    LOG_OVERHEAD = ...
    MAGIC_OFFSET = ...
    MIN_SLICE = ...
    def __init__(self, bytes_data: bytes) -> None: ...
    def size_in_bytes(self) -> int: ...
    def has_next(self) -> bool: ...
    def next_batch(
        self, _min_slice: int = ..., _magic_offset: int = ...
    ) -> DefaultRecordBatchProtocol | LegacyRecordBatchProtocol | None: ...

MemoryRecords: type[MemoryRecordsProtocol]
if NO_EXTENSIONS:
    MemoryRecords = ...
else:
    MemoryRecords = ...
