import struct
from hashlib import md5
from typing import Union

import aiohttp
from pytea import TEA
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from pyjce.buffer import ByteBuffer

server_pubkey = "04EBCA94D733E399B2DB96EACDD3F69A8BB0F74224E2B44E3357812211D2E62EFBC91BB553098E25E33A799ADC7F76FEB208DA7C6522CDB0719A305180CC54A82E"

tenKeyX = bytes.fromhex("EBCA94D733E399B2DB96EACDD3F69A8BB0F74224E2B44E3357812211D2E62EFB")
tenKeyY = bytes.fromhex("C91BB553098E25E33A799ADC7F76FEB208DA7C6522CDB0719A305180CC54A82E")


#
# class EncryptECDH:
#
#     def __init__(self, initial_sharekey=None, publickey=None, publickeyver=None):
#         self.initial_sharekey = initial_sharekey
#         self.publickey = publickey
#         self.publickeyver = publickeyver
#
#     def generate_key(self, spub_key: str) -> str:  # todo 完成
#         pub = bytes.fromhex(spub_key)
#
#     async def fetch_pubkey(self, uin: int):
#         async with aiohttp.ClientSession() as session:
#             async with session.get("https://keyrotate.qq.com/rotate_key?cipher_suite_ver=305&uin=" + str(uin)) as resp
#                 data = await resp.json()
#         self.publickeyver = data["PubKeyMeta"]["KeyVer"]
#         self.generate_key(data["PubKeyMeta"]["PubKey"])


class EncryptECDH:
    id = 0x87
    _p256 = ec.SECP256R1()

    svr_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        _p256,
        # bytes.fromhex(
        #     "04"
        #     "EBCA94D733E399B2DB96EACDD3F69A8BB0F74224E2B44E3357812211D2E62EFB"
        #     "C91BB553098E25E33A799ADC7F76FEB208DA7C6522CDB0719A305180CC54A82E"
        # )
        bytes([4]) + tenKeyX + tenKeyY
    )

    client_private_key = ec.generate_private_key(_p256)
    client_public_key = client_private_key.public_key().public_bytes(
        Encoding.X962, PublicFormat.UncompressedPoint
    )

    share_key = md5(
        client_private_key.exchange(ec.ECDH(), svr_public_key)[:16]
    ).digest()

    @classmethod
    def do_encrypt(
            cls, data: Union[bytes, bytearray], key: Union[bytes, bytearray]
    ) -> bytearray:
        b = ByteBuffer()
        b.write_bytes(struct.pack(">BB", 2, 1))
        b.write_bytes(key)
        b.write_bytes(struct.pack(
            ">HHH",
            305,
            1,  # oicq.wlogin_sdk.tools.EcdhCrypt.sKeyVersion
            len(cls.client_public_key)
        ))
        b.write_bytes(cls.client_public_key)
        b.write_bytes(TEA(cls.share_key).encrypt(bytes(data)))
        return b.bytes


ecdh = EncryptECDH()


class EncryptSession:
    id = 0x45

    def __init__(self, ticket: bytes):
        self.ticket = ticket  # t133

    def do_encrypt(
            self, data: Union[bytes, bytearray], key: Union[bytes, bytearray]
    ) -> bytes:
        return struct.pack(">H", len(self.ticket)) + self.ticket + TEA(bytes(key)).encrypt(bytes(data))
