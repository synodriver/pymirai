# -*- coding: utf-8 -*-
import asyncio

from pymirai.utils.pack import Pack


async def login(qq: int, password: str):
    reader, writer = await asyncio.open_connection("113.96.12.224", 8080)
    pack = Pack()
    pack.write_hex("00 00 06 B4 00 00 00 0A 02 00 00 00 04 00 00 00 00 0E")
    pack.write_qq(qq)
    writer.write(pack.get_all())
    await writer.drain()