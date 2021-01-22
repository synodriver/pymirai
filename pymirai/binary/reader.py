# -*- coding: utf-8 -*-
"""
tlv模块 TlvReader
"""
from typing import Union, Dict

from pyjce import ByteBuffer

DEFAULT_ENCODING = "utf-8"

TlvMap = Dict[int, Union[bytes, bytearray]]


class Reader:
    def __init__(self, data: Union[bytes, bytearray, ByteBuffer]):
        if isinstance(data, (bytes, bytearray)):
            self.buffer = ByteBuffer(data)
        elif isinstance(data, ByteBuffer):
            self.buffer = data
        else:
            raise TypeError(f"can't init Reader with data type {data.__class__.__name__}")

    def __len__(self) -> int:
        return len(self.buffer)

    def read_byte(self) -> bytearray:
        return self.buffer.read_bytes(1)

    def read_bytes(self, size: int) -> bytearray:
        return self.buffer.read_bytes(size)

    def read_bytes_short(self) -> bytearray:
        return self.read_bytes(self.read_uint16())

    def read_uint16(self) -> int:
        return self.buffer.read_uint2()

    def read_int32(self) -> int:
        return self.buffer.read_int4()

    def read_string(self) -> str:
        data = self.read_bytes(self.read_int32() - 4)
        return data.decode(DEFAULT_ENCODING)

    def read_string_short(self) -> str:
        data = self.read_bytes(self.read_uint16())
        return data.decode(DEFAULT_ENCODING)

    def read_string_limit(self, limit: int) -> str:
        data = self.read_bytes(limit)
        return data.decode(DEFAULT_ENCODING)

    def read_available(self) -> bytearray:
        return self.read_bytes(len(self.buffer))

    def read_tlv_map(self, tag_size: int) -> TlvMap:
        m = {}
        while True:
            if len(self) < tag_size:
                return m
            if tag_size == 1:
                k = self.read_byte()[0]
            elif tag_size == 2:
                k = self.read_uint16()
            elif tag_size == 4:
                k = self.read_int32()
            if k == 255:
                return m
            m[k] = self.read_bytes(self.read_uint16())
