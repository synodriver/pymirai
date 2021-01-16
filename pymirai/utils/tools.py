# -*- coding: utf-8 -*-
"""
操作字节流的
"""
import struct
import random


def int2bytes(num: int, outlen: int) -> bytes:
    return num.to_bytes(length=outlen, byteorder='big')


def bytes2int(bin_) -> int:
    return int.from_bytes(bin_, byteorder='big')


def hex2bytes(hexstr: str) -> bytes:
    str_bytes = hexstr.strip().replace("\n", "")
    pkt = bytes.fromhex(str_bytes)
    return pkt


def bytes2hex(bin_: bytes) -> str:
    return ''.join(['%02X ' % b for b in bin_])


def _bytes2hex(bin_: bytes) -> str:
    return bin_.hex().upper()


def str2bytes(text: str):
    return text.encode('utf-8')


def str2hex(text: str):
    strBytes = text.encode('utf-8')
    return bytes2hex(strBytes)


def hex2str(hexstr: str):
    strBytes = hexstr.split()
    pkt = bytearray(int(x, 16) for x in strBytes)
    return pkt.decode('utf-8')


def randbytes(num):
    int_list = [random.randint(0, 255) for i in range(num)]
    return bytes(int_list)
