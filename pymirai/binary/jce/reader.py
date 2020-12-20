# -*- coding: utf-8 -*-
import struct
from typing import Tuple

from .head import HeadData
from .buffer import ByteBuffer


class JceReader:
    """
    读取jce字节流
    """

    def __init__(self, data: bytes):
        self.buffer = ByteBuffer(data)

    def read_head(self) -> Tuple[HeadData, int]:
        """
        不仅康了,而且指针动了
        :return:
        """
        head_data = HeadData()
        b: int = self.buffer.read()
        head_data.type = b & 0x0F  # 低4位位类型
        head_data.tag = (b & 0xF0) >> 4  # 高4位为tag,
        if head_data.tag == 15:  # 如果tag为15 则下一个字段为tag
            b: int = self.buffer.read()
            head_data.tag = b & 0xFF  # TODO 这个似乎可以去掉 不过昵昵不改我也不改
            return head_data, 2
        else:
            return head_data, 1

    def peak_head(self) -> Tuple[HeadData, int]:
        """
        就康一眼
        :return:
        """
        return self.__class__(self.buffer.copy()).read_head()

    def skip(self, size: int) -> None:
        """
        跳过size个字节
        :param size:
        :return:
        """
        self.buffer.read_bytes(size)

    def skip_field(self, type_: int):
        """
        跳过一个字段 仅仅是跳过内容 这个头部还得你自己跳的
        see https://blog.csdn.net/jiange_zh/article/details/86562232
        :param type_:
        :return:
        """
        if type_ == 0:
            self.skip(1)
        elif type_ == 1:
            self.skip(2)
        elif type_ in (2, 4):
            self.skip(4)
        elif type_ in (3, 5):
            self.skip(8)
        elif type_ == 6:
            len_ = self.buffer.read()
            self.skip(len_)
        elif type_ == 7:
            len_ = self.buffer.read_int4()
            self.skip(len_)
        elif type_ == 8:
            pass
            # todo 一定要完成这个

    def skip_to_tag(self, tag: int) -> bool:
        while True:
            head, len_ = self.peak_head()
            if tag <= head.tag or head.type == 11:
                return tag == head.tag
            self.skip(len_)
            self.skip_field(head.type)

        pass


def main():
    pass


if __name__ == "__main__":
    main()
