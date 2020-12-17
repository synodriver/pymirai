# -*- coding: utf-8 -*-
import struct


def xor(a, b):
    op = 0xffffffff
    a1, a2 = struct.unpack(b'>LL', a[0:8])
    b1, b2 = struct.unpack(b'>LL', b[0:8])
    return struct.pack(b'>LL', (a1 ^ b1) & op, (a2 ^ b2) & op)


def tea_code(v, k):
    n = 16
    op = 0xffffffff
    delta = 0x9e3779b9
    k = struct.unpack(b'>LLLL', k[0:16])
    y, z = struct.unpack(b'>LL', v[0:8])
    s = 0
    for i in range(n):
        s += delta
        y += (op & (z << 4)) + k[0] ^ z + s ^ (op & (z >> 5)) + k[1]
        y &= op
        z += (op & (y << 4)) + k[2] ^ y + s ^ (op & (y >> 5)) + k[3]
        z &= op
    r = struct.pack(b'>LL', y, z)
    return r


def tea_decipher(v, k):
    n = 16
    op = 0xffffffff
    y, z = struct.unpack(b'>LL', v[0:8])
    a, b, c, d = struct.unpack(b'>LLLL', k[0:16])
    delta = 0x9E3779B9
    s = (delta << 4) & op
    for i in range(n):
        z -= ((y << 4) + c) ^ (y + s) ^ ((y >> 5) + d)
        z &= op
        y -= ((z << 4) + a) ^ (z + s) ^ ((z >> 5) + b)
        y &= op
        s -= delta
        s &= op
    return struct.pack(b'>LL', y, z)


class Tea:
    """QQ TEA 加解密, 64比特明码, 128比特密钥
这是一个确认线程安全的独立加密模块，使用时必须要有一个全局变量secret_key，要求大于等于16位
    """

    @staticmethod
    def encrypt(v: bytes, secret_key: bytes):
        END_CHAR = b'\0'
        FILL_N_OR = 0xF8
        vl = len(v)
        filln = (8 - (vl + 2)) % 8 + 2
        fills = b''
        for i in range(filln):
            fills = fills + bytes([220])
        v = (bytes([(filln - 2) | FILL_N_OR])
             + fills
             + v
             + END_CHAR * 7)
        tr = b'\0' * 8
        to = b'\0' * 8
        r = b''
        o = b'\0' * 8
        for i in range(0, len(v), 8):
            o = xor(v[i:i + 8], tr)
            tr = xor(tea_code(o, secret_key), to)
            to = o
            r += tr
        return r

    @staticmethod
    def decrypt(v: bytes, secret_key: bytes):
        l = len(v)
        prePlain = tea_decipher(v, secret_key)
        pos = (prePlain[0] & 0x07) + 2
        r = prePlain
        preCrypt = v[0:8]
        for i in range(8, l, 8):
            x = xor(tea_decipher(xor(v[i:i + 8], prePlain), secret_key), preCrypt)
            prePlain = xor(x, preCrypt)
            preCrypt = v[i:i + 8]
            r += x
        if r[-7:] != b'\0' * 7:
            return None
        return r[pos + 1:-7]

# if __name__ == '__main__':
#     global secret_key
#     secret_key = hex2bytes('11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11')
#     print(bytes2hex(secret_key))

#     QQ = TEA()

#     plaintext = '哈哈哈hhh,'
#     plaintext = bytes(plaintext,encoding = "utf-8")
#     enc = QQ.encrypt(plaintext)
#     print(bytes2hex(enc))
#     dec = QQ.decrypt(enc)
#     print(bytes2hex(dec))
