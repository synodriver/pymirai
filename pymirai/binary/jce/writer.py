# -*- coding: utf-8 -*-
from typing import Union, List, Optional, Any, MutableMapping

from pydantic import BaseModel

from .buffer import ByteBuffer
from .struct import IJceStruct

DEFAULT_ENCODING = "utf-8"


class JceWriter:
    """
    写入jce字节流
    """

    def __init__(self, data: Optional[Union[bytes, bytearray, ByteBuffer]] = None):
        if data is None:
            self.buffer = ByteBuffer()
        elif isinstance(data, (bytes, bytearray)):
            self.buffer = ByteBuffer(data)
        elif isinstance(data, ByteBuffer):
            self.buffer = data
        else:
            raise TypeError(f"can't init JceWriter with data type {data.__class__.__name__}")

    def write_head(self, type_: int, tag: int) -> None:
        """

        :param type_:
        :param tag:
        :return:
        """
        if tag < 15:
            data = bytes([tag << 4 | type_])  # go的byte就是uint8
            self.buffer.write_bytes(data)
        elif tag < 256:
            data = bytes([0xFF | type_])
            self.buffer.write_bytes(data)
            self.buffer.write_bytes(bytes([tag]))

    def write_byte(self, b: bytes, tag: int) -> None:
        """
        写入一个字节
        :param b:
        :param tag:
        :return:
        """
        if len(b) != 1:
            raise ValueError("write_byte only accept single byte")
        if b[0] == 0:
            self.write_head(12, tag)
        else:
            self.write_head(0, tag)
            self.buffer.write_bytes(b)

    def write_bool(self, b: bool, tag: int) -> None:
        if b:
            data: bytes = bytes([1])
        else:
            data: bytes = bytes([0])
        self.write_byte(data, tag)

    def write_int16(self, n: int, tag: int) -> None:
        if -128 <= n <= 127:
            self.write_byte(bytes([n]), tag)
            return
        self.write_head(1, tag)
        self.buffer.write_int2(n)

    def write_int32(self, n: int, tag: int) -> "JceWriter":
        if -32768 <= n <= 32767:
            self.write_int16(n, tag)
            return self
        self.write_head(2, tag)
        self.buffer.write_int4(n)
        return self

    def write_int64(self, n: int, tag: int) -> "JceWriter":
        if -2147483648 <= n <= 2147483647:
            return self.write_int32(n, tag)
        self.write_head(3, tag)
        self.buffer.write_int8(n)
        return self

    def write_float32(self, n: float, tag: int):
        self.write_head(4, tag)
        self.buffer.write_float(n)

    def write_float64(self, n: float, tag: int):  # 就是double
        self.write_head(5, tag)
        self.buffer.write_double(n)

    def write_string(self, s: str, tag: int) -> "JceWriter":
        """
        type 6 or 7 >255就得7了
        :param s:
        :param tag:
        :return:
        """
        by: bytes = s.encode(DEFAULT_ENCODING)
        if len(by) > 255:
            self.write_head(7, tag)
            self.buffer.write_bytes(len(by).to_bytes(4, "big"))  # 4个字节的长度
            self.buffer.write_bytes(by)
            return self
        self.write_head(6, tag)
        self.buffer.write_bytes(bytes([len(by)]))  # 1byte
        self.buffer.write_bytes(by)
        return self

    def write_bytes(self, data: Union[bytes, bytearray], tag: int):
        self.write_head(13, tag)
        self.write_head(0, 0)
        self.write_int32(len(data), 0)
        self.buffer.write_bytes(data)

    def write_int64_list(self, data: List[int], tag: int):
        """
        go: WriteInt64Slice
        :param data:
        :param tag:
        :return:
        """
        self.write_head(9, tag)
        if len(data) == 0:
            self.write_int32(0, 0)
            return
        self.write_int32(len(data), 0)
        for i in data:
            self.write_int64(i, 0)

    def write_list(self, data: List[Any], tag: int):
        if not isinstance(data, list):
            return
        self.write_head(9, tag)
        if len(data) == 0:
            self.write_int32(0, 0)
            return
        self.write_int32(len(data), 0)
        for i in data:
            self.write_object(i, 0)  # todo 没完成

    def write_jce_struct_list(self, data: List[IJceStruct], tag: int):
        self.write_head(9, tag)
        if len(data) == 0:
            self.write_int32(0, 0)
            return
        self.write_int32(len(data), 0)
        for i in data:
            self.write_jce_struct(i, 0)

    def write_map(self, m: dict, tag: int):
        if not m:
            self.write_head(8, tag)
            self.write_int32(0, 0)
            return
        if not isinstance(map, MutableMapping):
            return
        self.write_head(8, tag)
        self.write_int32(len(m), 0)
        for k, v in m.items():
            self.write_object(k, 0)
            self.write_object(v, 1)

    def write_object(self, data: Any, tag: int):
        if isinstance(data, MutableMapping):
            self.write_map(data, tag)
            return
        if isinstance(data, list):
            self.write_list(data, tag)
            return
        if isinstance(data, (bytes, bytearray)):
            self.write_bytes(data, tag)
            return
        if isinstance(data, bool):
            self.write_bool(data, tag)
        elif isinstance(data, int):
            self.write_int64(data, tag)
        elif isinstance(data, float):
            self.write_float64(data, tag)
        elif isinstance(data, str):
            self.write_string(data, tag)
        elif isinstance(data, IJceStruct):  # todo 还有个basemodel
            self.write_jce_struct(data, tag)

    def write_jce_struct_raw(self, data: Union[IJceStruct, BaseModel]):
        """
        todo 用pydantic给前面的都写加上jceid元数据 不然没法玩
        :param data:
        :return:
        """
        for field_name, val in data.schema()["properties"].items():
            jce_id: int = val["jce_id"]
            self.write_object(getattr(data, field_name), jce_id)

    def write_jce_struct(self, data: IJceStruct, tag: int):
        self.write_head(10, tag)
        self.write_jce_struct_raw(data)
        self.write_head(11, 0)

    def bytes(self) -> bytearray:
        return self.buffer.bytes
