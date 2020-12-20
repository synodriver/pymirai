# -*- coding: utf-8 -*-
import asyncio
from pymirai.protocol.AndroidQQ import AndroidQQ
from pymirai.utils.pack import Pack
from pymirai.utils.tools import bytes2hex

Loginqq = AndroidQQ('2193096276', 'dwg20010417', 0)


async def login():
    reader, writer = await asyncio.open_connection("113.96.12.224", 8080)

    writer.write(Loginqq.Pack_Login())
    await writer.drain()
    buf = await reader.read(2048)
    print(bytes2hex(buf))
    print(Loginqq.Unpack_Login(buf))
    writer.close()
    await writer.wait_closed()

    from pymirai.protocol.AndroidQQ import AndroidQQ

    # print(bytes2hex(int2bytes(2193096276,4)))


asyncio.run(login())
