# -*- coding: utf-8 -*-

def gen_uuid(uuid: bytes) -> str:
    u: bytes = uuid[0:16]
    buf: str = ""
    buf += ''.join(['%02X ' % b for b in u[0:4]])
    buf += "-"
    buf += ''.join(['%02X ' % b for b in u[4:6]])
    buf += "-"
    buf += ''.join(['%02X ' % b for b in u[6:8]])
    buf += "-"
    buf += ''.join(['%02X ' % b for b in u[8:10]])
    buf += "-"
    buf += ''.join(['%02X ' % b for b in u[10:16]])
    return buf
