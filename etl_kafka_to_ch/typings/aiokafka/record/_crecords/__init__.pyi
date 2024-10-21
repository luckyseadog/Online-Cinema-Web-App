"""
This type stub file was generated by pyright.
"""

from .cutil import crc32c_cython, decode_varint_cython, encode_varint_cython, size_of_varint_cython
from .default_records import DefaultRecord, DefaultRecordBatch, DefaultRecordBatchBuilder, DefaultRecordMetadata
from .legacy_records import LegacyRecord, LegacyRecordBatch, LegacyRecordBatchBuilder, LegacyRecordMetadata
from .memory_records import MemoryRecords

__all__ = [
    "DefaultRecord",
    "DefaultRecordBatch",
    "DefaultRecordBatchBuilder",
    "DefaultRecordMetadata",
    "LegacyRecord",
    "LegacyRecordBatch",
    "LegacyRecordBatchBuilder",
    "LegacyRecordMetadata",
    "MemoryRecords",
    "crc32c_cython",
    "decode_varint_cython",
    "encode_varint_cython",
    "size_of_varint_cython",
]
