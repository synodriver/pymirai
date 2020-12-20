# -*- coding: utf-8 -*-
"""
jce field 的头部 tag type
"""
from typing import Optional


class HeadData(object):
    """
    ttlv的头部信息
    tag1 type [tag2] length value需要处理
    """

    def __init__(self, tag: Optional[int] = 0, type_: Optional[int] = 0):
        if tag < 256:
            self.tag = tag
        else:
            raise ValueError("tag can't greater than 255")
        self.type = type_

    def __str__(self):
        return '{tag: %d, type: %d}' % (self.tag, self.type)

    def __repr__(self):
        return '{tag: %d, type: %d}' % (self.tag, self.type)

    def as_dict(self):
        return {"tag": self.tag, "type": self.type}

    def as_bytes(self) -> bytes:
        """
        转化为二进制用于写入
        :return: 要么1字节 要么2字节
        """
        if self.tag < 15:
            return bytes([self.tag << 4 | self.type])
        else:
            return bytes([15 | self.type]) + bytes([self.tag])

    def clear(self):
        self.tag = 0
        self.type = 0
