# -*- coding: utf-8 -*-
import asyncio
import socket

CHUNK_SIZE = -1


class TCPConnection:
    """
    对流的封装 方便处理
    """

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.buffer = b""
        self.closed = False
        self.reader = reader
        self.writer = writer
        self.socket: socket.socket = writer.get_extra_info("socket")

    def __str__(self):
        return f"TCPConnection to {self.peername}"

    @classmethod
    async def new(cls, host: str, port: int, **kw) -> "TCPConnection":
        reader, writer = await asyncio.open_connection(host, port, **kw)
        return cls(reader, writer)

    @property
    def peername(self):
        return self.writer.get_extra_info('peername')

    def add_into_buffer(self, data: bytes) -> None:
        self.buffer += data

    def recv(self, size: int = CHUNK_SIZE) -> bytes:
        return self.socket.recv(size)

    def send(self, data: bytes) -> int:
        return self.socket.send(data)

    async def read(self, size: int = CHUNK_SIZE) -> bytes:
        return await self.reader.read(size)

    def write(self, data: bytes) -> None:
        self.writer.write(data)

    async def drain(self) -> None:
        await self.writer.drain()

    async def flush(self):
        self.write(self.buffer)
        self.buffer = b""
        await self.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.closed = True
