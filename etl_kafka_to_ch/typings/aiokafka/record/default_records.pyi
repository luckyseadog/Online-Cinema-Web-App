"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Any, final
from collections.abc import Callable, Sized
from typing import Self
from aiokafka.util import NO_EXTENSIONS
from ._protocols import (
    DefaultRecordBatchBuilderProtocol,
    DefaultRecordBatchProtocol,
    DefaultRecordMetadataProtocol,
    DefaultRecordProtocol,
)
from ._types import CodecGzipT, CodecLz4T, CodecMaskT, CodecNoneT, CodecSnappyT, CodecZstdT

class DefaultRecordBase:
    __slots__ = ...
    HEADER_STRUCT = ...
    ATTRIBUTES_OFFSET = ...
    CRC_OFFSET = ...
    AFTER_LEN_OFFSET = ...
    CODEC_MASK: CodecMaskT = ...
    CODEC_NONE: CodecNoneT = ...
    CODEC_GZIP: CodecGzipT = ...
    CODEC_SNAPPY: CodecSnappyT = ...
    CODEC_LZ4: CodecLz4T = ...
    CODEC_ZSTD: CodecZstdT = ...
    TIMESTAMP_TYPE_MASK = ...
    TRANSACTIONAL_MASK = ...
    CONTROL_MASK = ...
    LOG_APPEND_TIME = ...
    CREATE_TIME = ...
    NO_PARTITION_LEADER_EPOCH = ...

@final
class _DefaultRecordBatchPy(DefaultRecordBase, DefaultRecordBatchProtocol):
    def __init__(self, buffer: bytes | bytearray | memoryview) -> None: ...
    @property
    def base_offset(self) -> int: ...
    @property
    def magic(self) -> int: ...
    @property
    def crc(self) -> int: ...
    @property
    def attributes(self) -> int: ...
    @property
    def compression_type(self) -> int: ...
    @property
    def timestamp_type(self) -> int: ...
    @property
    def is_transactional(self) -> bool: ...
    @property
    def is_control_batch(self) -> bool: ...
    @property
    def last_offset_delta(self) -> int: ...
    @property
    def first_timestamp(self) -> int: ...
    @property
    def max_timestamp(self) -> int: ...
    @property
    def producer_id(self) -> int: ...
    @property
    def producer_epoch(self) -> int: ...
    @property
    def base_sequence(self) -> int: ...
    @property
    def next_offset(self) -> int: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> _DefaultRecordPy: ...
    def validate_crc(self) -> bool: ...

@final
@dataclass(frozen=True)
class _DefaultRecordPy(DefaultRecordProtocol):
    __slots__ = ...
    offset: int
    timestamp: int
    timestamp_type: int
    key: bytes | None
    value: bytes | None
    headers: list[tuple[str, bytes | None]]
    @property
    def checksum(self) -> None: ...

@final
class _DefaultRecordBatchBuilderPy(DefaultRecordBase, DefaultRecordBatchBuilderProtocol):
    MAX_RECORD_OVERHEAD = ...
    def __init__(
        self,
        magic: int,
        compression_type: int,
        is_transactional: int,
        producer_id: int,
        producer_epoch: int,
        base_sequence: int,
        batch_size: int,
    ) -> None: ...
    def append(
        self,
        offset: int,
        timestamp: int | None,
        key: bytes | None,
        value: bytes | None,
        headers: list[tuple[str, bytes | None]],
        encode_varint: Callable[[int, Callable[[int], None]], int] = ...,
        size_of_varint: Callable[[int], int] = ...,
        get_type: Callable[[Any], type] = ...,
        type_int: type[int] = ...,
        time_time: Callable[[], float] = ...,
        byte_like: tuple[type[bytes], type[bytearray], type[memoryview]] = ...,
        bytearray_type: type[bytearray] = ...,
        len_func: Callable[[Sized], int] = ...,
        zero_len_varint: int = ...,
    ) -> _DefaultRecordMetadataPy | None:
        """Write message to messageset buffer with MsgVersion 2"""

    def build(self) -> bytearray: ...
    def size(self) -> int:
        """Return current size of data written to buffer"""

    def size_in_bytes(
        self,
        offset: int,
        timestamp: int,
        key: bytes | None,
        value: bytes | None,
        headers: list[tuple[str, bytes | None]],
    ) -> int: ...
    @classmethod
    def size_of(cls, key: bytes | None, value: bytes | None, headers: list[tuple[str, bytes | None]]) -> int: ...
    @classmethod
    def estimate_size_in_bytes(
        cls, key: bytes | None, value: bytes | None, headers: list[tuple[str, bytes | None]]
    ) -> int:
        """Get the upper bound estimate on the size of record"""

    def set_producer_state(self, producer_id: int, producer_epoch: int, base_sequence: int) -> None: ...
    @property
    def producer_id(self) -> int: ...
    @property
    def producer_epoch(self) -> int: ...
    @property
    def base_sequence(self) -> int: ...

@final
@dataclass(frozen=True)
class _DefaultRecordMetadataPy(DefaultRecordMetadataProtocol):
    __slots__ = ...
    offset: int
    size: int
    timestamp: int
    @property
    def crc(self) -> None: ...

DefaultRecordBatchBuilder: type[DefaultRecordBatchBuilderProtocol]
DefaultRecordMetadata: type[DefaultRecordMetadataProtocol]
DefaultRecordBatch: type[DefaultRecordBatchProtocol]
DefaultRecord: type[DefaultRecordProtocol]
if NO_EXTENSIONS:
    DefaultRecordBatchBuilder = ...
    DefaultRecordMetadata = ...
    DefaultRecordBatch = ...
    DefaultRecord = ...
else:
    DefaultRecordBatchBuilder = ...
    DefaultRecordMetadata = ...
    DefaultRecordBatch = ...
    DefaultRecord = ...
