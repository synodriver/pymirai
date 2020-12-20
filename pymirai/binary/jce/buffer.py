# -*- coding: utf-8 -*-
import struct
from typing import Optional


class ByteBuffer:
    """
    字节缓冲区
    """

    # _bytes = None
    # _position = 0

    def __init__(self, bs: Optional[bytes] = None):
        if bs is None:
            self._bytes = b""
        elif isinstance(bs, bytes):
            self._bytes = bs
        elif isinstance(bs, bytearray):
            self._bytes = bytes(bs)
        else:
            raise TypeError("'buffer' argument must be bytes or bytesarray")
        self._position = 0

    @property
    def bytes(self) -> bytes:
        """
        返回自己的全部数据
        :return:
        """
        return self._bytes

    @property
    def position(self):
        """
        位置指针 当前读取的字节数 读取到第几个字节了
        :return:
        """
        return self._position

    @position.setter
    def position(self, value):
        """
        设置读取指针
        :param value:
        :return:
        """
        if not isinstance(value, int):
            raise TypeError("'position' attribute must be a integer")
        elif value < 0:
            raise ValueError("'position' attribute must be a positive number")
        elif value > len(self._bytes):
            raise ValueError('position out of index range')
        else:
            self._position = value

    def read(self) -> int:
        """
        读取一个字节并返回 指针+1
        :return:
        """
        if self._position >= len(self._bytes):
            raise BufferError('reached end of bytes')
        b = self._bytes[self._position]
        self._position += 1
        return b

    def read_bytes(self, size: int) -> bytes:
        """
        读取接下来的size个字节 指针向后面移动size
        :param size:
        :return:
        """
        if size < 0:
            raise ValueError("'size' attribute must be a positive number")
        if self._position > len(self._bytes):
            raise BufferError('reached end of bytes')
        if self.position + size > len(self._bytes):
            raise BufferError('reached end of bytes')
        b = self._bytes[self.position:self.position + size]
        self.position = self.position + size
        return b

    def read_int2(self) -> int:
        """
        读取一个jce中的int2类型
        :return:
        """
        b = self.read_bytes(2)
        return struct.unpack('>h', b)[0]  # 解包出来是个元组 得像这样加料

    def read_int4(self) -> int:
        """
        读取一个jce中的int4类型
        :return:
        """
        b = self.read_bytes(4)
        return struct.unpack('>i', b)[0]

    def read_int8(self) -> int:
        """
        读取一个jce中的int8类型
        :return:
        """
        b = self.read_bytes(8)
        return struct.unpack('>q', b)[0]

    def read_float(self) -> float:
        """
        读取一个jce中的float类型 4字节
        :return:
        """
        b = self.read_bytes(4)
        return struct.unpack('>f', b)[0]

    def read_double(self) -> float:
        """
        读取一个jce中的double类型 8字节
        :return:
        """
        b = self.read_bytes(8)
        return struct.unpack('>d', b)[0]

    def write_bytes(self, data: bytes) -> None:
        """
        写入一个字节流
        :param data:
        :return:
        """
        self._bytes += data
        self._position += len(data)

    def write_hex(self, hexstr: str) -> None:
        str_bytes: str = hexstr.strip()
        pkt = bytes.fromhex(str_bytes)
        self.write_bytes(pkt)

    def write_int2(self, num):
        pkt = struct.pack(">h", num)
        self.write_bytes(pkt)

    def write_int4(self, num):
        pkt = struct.pack(">i", num)
        self.write_bytes(pkt)

    def write_int8(self, num):
        pkt = struct.pack(">q", num)
        self.write_bytes(pkt)

    def write_float(self, num):
        pkt = struct.pack(">f", num)
        self.write_bytes(pkt)

    def write_double(self, num):
        pkt = struct.pack(">d", num)
        self.write_bytes(pkt)

    def copy(self):
        """
        返回自己的一份深拷贝
        :return:
        """
        bb = ByteBuffer(self._bytes)
        bb.position = self.position
        return bb

    def seek(self, position: int) -> None:
        """
        重新定位指针
        :param position:
        :return:
        """
        self.position = position

    def clear(self) -> None:
        """
        指针重新回到0
        :return:
        """
        self._position = 0
