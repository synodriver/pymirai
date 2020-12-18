# -*- coding: utf-8 -*-
"""
python的二进制操作太挫了 需要加以改进
"""


class Pack(object):
    """
    组包
    """

    def __init__(self):
        self.buffer = bytes()

    def set_empty(self) -> None:
        """
        清空
        :return:
        """
        self.buffer = bytes()

    def get_all(self) -> bytes:
        """
        返回全部流
        :return:
        """
        return self.buffer

    def write_hex(self, hexstr: str) -> None:
        str_bytes: str = hexstr.strip()
        pkt = bytes.fromhex(str_bytes)
        self.buffer += pkt

    def write_int(self, num: int) -> None:
        pkt = num.to_bytes(length=4, byteorder='big')
        self.buffer += pkt

    def write_short(self, num) -> None:
        pkt = int(num).to_bytes(length=2, byteorder='big')  # , signed=True)
        self.buffer += pkt

    def write_str(self, text: str, encoding:str="utf-8") -> None:
        pkt = text.encode(encoding)
        self.buffer += pkt

    def write_bytes(self, byte: bytes) -> None:
        self.buffer += byte

    def write_qq(self, qq: int) -> None:
        """
        编码qq  12345   -> 31 32 33 34 35
        :param qq:
        :return:
        """
        _qq = map(int, str(qq))
        pkt: bytes = b"".join(bytes([48 | i]) for i in _qq)
        self.buffer += pkt

    def set_login_token(self, byte) -> None:
        pass

    def set_token(self, byte) -> None:
        pass
