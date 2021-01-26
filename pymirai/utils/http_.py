# -*- coding: utf-8 -*-
import gzip

import aiohttp

data = b'\x95\x1bw\xcf(\x13L\x1f\\%O\xc0\xfe\x1eI>[\xf5&\xec\x89.\xd1\x0b\x0f\xe3!<\x14}Q\x10\x162\xd1\xb6\xe9n\x80\xf6\x1b\xe8V\xb4\xf0\xfd\xcf#\xf9\xd5X\xd8\xb4\xb7{\x15\xccVx\x90\xe4\x94$\xba\xc6f\x00\x97\x0f9\x18\x18\xe4\xcf\xc1\x1d\xa6\xb2\xa4\xd8\x96\x97\xb0B\x92\xa5*|\xf9\x16\xe0\x19\t\x17\x06\xb0=}.\x19\xdd\xc7=\x19\xeb\xe6\xecO\xec\xac2Skib\x12F\x04\x02\xf9G\xb9Up?\xc5\xf6\xde\xb96\xdf\x18\x89\xbe\x04rl\xc2\x01\xde\xfb\xcb\xb1\xa9\xa0\xd7\x180\xeeC\x9f\\\xd7u}b:]\xd4C8\xdc@^\x08\x96\xe1\x8e'


async def http_post_bytes(url: str, data: bytes) -> bytes:
    headers = {"User-Agent": "QQ/8.2.0.1296 CFNetwork/1126", "Net-Type": "Wifi"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as resp:
            body = await resp.read()
            if "gzip" in resp.headers.get("Content-Encoding", ""):
                uncom = gzip.decompress(body)
                return uncom
            return body


if __name__ == "__main__":
    import asyncio

    asyncio.run(http_post_bytes("https://configsvr.msf.3g.qq.com/configsvr/serverlist.jsp",data))
