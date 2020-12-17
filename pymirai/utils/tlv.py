# -*- coding: utf-8 -*-
from .pack import Pack


class Tlv(object):
    """
    工具类
    """
    def __init__(self):
        pass

    @staticmethod
    def tlv_pack(cmd, bin_):
        pack = Pack()
        pack.write_hex(cmd)
        pack.write_short(len(bin_))
        pack.write_bytes(bin_)

    @staticmethod
    def tlv018(qq: str):
        pack = Pack()
        pack.write_hex('00 01 00 00 06 00 00 00 00 10 00 00 00 00')
        pack.write_int(int(qq))
        pack.write_bytes(bytes(4))
        return Tlv.tlv_pack('00 18', pack.get_all())
