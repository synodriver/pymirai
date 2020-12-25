# -*- coding: utf-8 -*-
"""
https://tarscloud.github.io/TarsDocs/base/tars-protocol.html
"""
from typing import Tuple, Union, Callable, Any

from .head import HeadData
from .buffer import ByteBuffer

DEFAULT_ENCODING = "utf-8"


class JceReader:
    """
    读取jce字节流
    """

    def __init__(self, data: Union[bytes, bytearray, ByteBuffer]):
        if isinstance(data, (bytes, bytearray)):
            self.buffer = ByteBuffer(data)
        elif isinstance(data, ByteBuffer):
            self.buffer = data
        else:
            raise TypeError(f"can't init JceReader with data type {data.__class__.__name__}")

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

    def _skip_field(self, type_: int):
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
        elif type_ == 8:  # map
            size: int = self.read_int32(0)
            for i in range(2 * size):
                self.skip_next_field()
        elif type_ == 9:  # list
            size: int = self.read_int32(0)
            for i in range(size):
                self.skip_next_field()
        elif type_ == 10:
            self.skip_to_struct_end()
        elif type_ == 13:
            self.read_head()
            size: int = self.read_int32(0)
            self.skip(size)

    def skip_next_field(self):
        head, _ = self.read_head()
        self._skip_field(head.type)

    def skip_field(self, count: int):
        for i in range(count):
            self.skip_next_field()

    def read_bytes(self, size: int) -> bytearray:
        b = self.buffer.read_bytes(size)
        return b

    def _read_byte(self) -> bytes:
        """
        一个字节
        :return:
        """
        return self.read_bytes(1)

    def read_uint16(self) -> int:
        return self.buffer.read_int2()

    def _read_int32(self) -> int:
        return self.buffer.read_int4()

    def _read_int64(self) -> int:
        return self.buffer.read_int8()

    def _read_float32(self) -> float:
        return self.buffer.read_float()

    def _read_float64(self) -> float:
        return self.buffer.read_double()

    def skip_to_tag(self, tag: int) -> bool:
        """
        跳转到tag
        :param tag:
        :return:
        """
        while True:
            head, len_ = self.peak_head()
            if tag <= head.tag or head.type == 11:
                return tag == head.tag
            self.skip(len_)
            self._skip_field(head.type)

    def skip_to_struct_end(self):
        while True:
            head, _ = self.read_head()
            self._skip_field(head.type)
            if head.type == 11:
                return

    def read_byte(self, tag: int) -> bytes:
        if not self.skip_to_tag(tag):
            return bytes([0])
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return bytes([0])
        elif type_ == 0:
            return self._read_byte()
        else:
            return bytes([0])

        pass

    def read_bool(self, tag: int) -> bool:
        return self.read_bytes(tag) != 0

    def read_int16(self, tag: int) -> int:
        if not self.skip_to_tag(tag):
            return 0
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return 0
        elif type_ == 0:
            return self._read_byte()[0]
        elif type_ == 1:
            return self.read_uint16()
        else:
            return 0

    def read_int32(self, tag: int) -> int:
        if not self.skip_to_tag(tag):
            return 0
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return 0
        elif type_ == 0:
            return self._read_byte()[0]
        elif type_ == 1:
            return self.read_uint16()
        elif type_ == 2:
            return self._read_int32()
        else:
            return 0

    def read_int64(self, tag: int) -> int:
        if not self.skip_to_tag(tag):
            return 0
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return 0
        elif type_ == 0:
            return self._read_byte()[0]
        elif type_ == 1:
            return self.read_uint16()
        elif type_ == 2:
            return self._read_int32()
        elif type_ == 3:
            return self._read_int64()
        else:
            return 0

    def read_float32(self, tag: int) -> float:
        if not self.skip_to_tag(tag):
            return 0.0
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return 0.0
        elif type_ == 4:
            return self._read_float32()
        else:
            return 0.0

    def read_float64(self, tag: int):
        if not self.skip_to_tag(tag):
            return 0.0
        head, _ = self.read_head()
        if (type_ := head.type) == 12:
            return 0.0
        elif type_ == 4:
            return self._read_float32()
        elif type_ == 5:
            return self._read_float64()
        else:
            return 0.0
        pass

    def read_string(self, tag: int):
        if not self.skip_to_tag(tag):
            return ""
        head, _ = self.read_head()
        if (type_ := head.type) == 6:
            return self.read_bytes(self._read_byte()[0]).decode(DEFAULT_ENCODING)
        elif type_ == 7:
            return self.read_bytes(self._read_int32()).decode(DEFAULT_ENCODING)
        else:
            return ""

    # ReadAny Read any type via tag, unsupported JceStruct
    def read_any(self, tag: int) -> Any:
        if not self.skip_to_tag(tag):
            return
        head, _ = self.read_head()
        if (type_ := head.type) == 0:
            return self._read_byte()[0]
        elif type_ == 1:
            return self.read_uint16()
        elif type_ == 2:
            return self._read_int32()
        elif type_ == 3:
            return self._read_int64()
        elif type_ == 4:
            return self._read_float32()
        elif type_ == 5:
            return self._read_float64()
        elif type_ == 6:
            return self.read_bytes(self._read_byte()[0]).decode(DEFAULT_ENCODING)
        elif type_ == 7:
            return self.read_bytes(self._read_int32()).decode(DEFAULT_ENCODING)
        elif type_ == 8:  # map csdn的文档大有问题
            size: int = self.read_int32(0)  # 跳到字典
            m = {}
            for i in range(size):
                k = self.read_any(0)  # 不这么写会出问题
                v = self.read_any(1)
                m[k] = v
            return m
        elif type_ == 9:  # list
            sl = []
            size = self.read_int32(0)
            for i in range(size):
                sl.append(self.read_any(0))
            return sl
        elif type_ == 10:  # obj
            sl = []
            while True:
                head, _ = self.peak_head()
                if head.type == 11 and head.tag == 0:
                    break
                sl.append(self.read_any(head.tag))
            return sl

        elif type_ == 11:
            return None

        elif type_ == 12:
            return 0
        elif type_ == 13:  # simple list   head len data
            self.read_head()
            return self.read_bytes(self.read_int32(0))
        else:
            return

    def read_map_f(self, tag: int, func: Callable[[Any, Any], Any]) -> None:
        if not self.skip_to_tag(tag):
            return
        self.read_head()  # 去头就可以吃了
        size = self.read_int32(0)
        for i in range(size):
            k = self.read_any(0)
            v = self.read_any(1)
            if k is not None:
                func(k, v)

    def read_list(self, tag: int):
        if not self.skip_to_tag(tag):
            return
        head, _ = self.read_head()
        if head.type == 9:
            sl = []
            size = self.read_int32(0)
            for i in range(size):
                sl.append(self.read_any(0))
            return sl
        elif head.type == 13:  # simple list   head len data
            self.read_head()
            return self.read_bytes(self.read_int32(0))

    def read_object(self, tag: int):
        """
        读取自定义结构
        :param tag:
        :return:
        """
        if not self.skip_to_tag(tag):
            return
        ls = []
        head, _ = self.read_head()  # 去头就可以吃了
        if head.type != 10:
            return ls
        head, _ = self.read_head()
        tag = head.tag
        while True:
            data = self.read_any(tag)
            if data:
                ls.append(data)
            tag += 1

    def read_available(self) -> bytes:
        """
        读取全部缓冲区剩下的
        :return:
        """
        self.read_bytes(len(self.buffer) - self.buffer.position)
