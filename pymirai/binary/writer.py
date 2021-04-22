# -*- coding: utf-8 -
"""
tlv writer
"""
from typing import Union, Optional, Callable

from pyjce import ByteBuffer

try:
    from pytea import TEA  # C写的
except ImportError:
    from pymirai.binary.tea import TEA  # py写的


class Writer:
    def __init__(self, data: Optional[Union[bytes, bytearray, ByteBuffer]] = None):
        if data is None:
            self.buffer = ByteBuffer()
        elif isinstance(data, (bytes, bytearray)):
            self.buffer = ByteBuffer(data)
        elif isinstance(data, ByteBuffer):
            self.buffer = data
        else:
            raise TypeError(f"can't init Writer with data type {data.__class__.__name__}")

    def write(self, data: bytes):
        """写入多字节"""
        self.buffer.write_bytes(data)

    def write_byte(self, data: int):
        """写入1字节"""
        self.buffer.write_bytes(bytes([data]))

    def write_uint16(self, data: int):
        self.buffer.write_uint2(data)

    def write_uint32(self, data: int):
        self.buffer.write_uint4(data)

    def write_uint64(self, data: int):
        self.buffer.write_uint8(data)

    def write_string(self, data: str):
        payload = data.encode()
        self.write_uint32(len(payload) + 4)
        self.write(payload)

    def write_string_short(self, data: str):
        self.write_tlv(data.encode())

    def write_bool(self, b: bool):
        self.write_byte(0x01) if b else self.write_byte(0x00)

    def encrypt_and_write(self, key: bytes, data: bytes):
        tea = TEA(key)
        encrypted = tea.encrypt(data)
        self.write(encrypted)

    def write_int_lv_packet(self, offset: int, f: Callable[["Writer"], None]) -> None:
        t = self.__class__()
        f(t)
        data = t.bytes()
        self.write_uint32(len(data) + offset)
        self.write(data)

    def write_uni_packet(self, command_name: str, session_id: bytes, extra_data: bytes, body: bytes) -> None:
        def _lambda_1(w: "Writer"):
            w.write_string(command_name)
            w.write_uint32(8)
            w.write(session_id)
            if len(extra_data) == 0:
                w.write_uint32(0x04)
            else:
                w.write_uint32(len(extra_data) + 4)
                w.write(extra_data)

        self.write_int_lv_packet(4, _lambda_1)

        def _lambda_2(w: "Writer"):
            w.write(body)

        self.write_int_lv_packet(4, _lambda_2)

    def write_tlv(self, data: bytes):
        self.write_uint16(len(data))
        self.write(data)

    def write_tlv_limited_size(self, data: bytes, limit: int):
        if len(data) <= limit:
            self.write_tlv(data)
            return
        self.write_tlv(data[:limit])

    def bytes(self) -> bytearray:
        return self.buffer.bytes
