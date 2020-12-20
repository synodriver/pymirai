# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from pymirai.utils.tools import *
from pymirai.utils.pack import Pack
from pymirai.utils.tea import Tea


class TestPack(TestCase):

    def test_pack(self):
        a = bytes2hex(Tea.encrypt(str2bytes('哈哈哈'), hex2bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
        # print(a)
        b = bytes2hex(Tea.decrypt(hex2bytes(a), hex2bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
        self.assertEqual(hex2str(b), "哈哈哈")
        p = Pack()
        p.write_qq(123456)
        self.assertEqual(p.get_all(), hex2bytes("31 32 33 34 35 36"))

    def test_decode(self):
        with open("data.txt") as f:
            a = f.read().strip()
        data = Tea.decrypt((hex2bytes(a)), bytes(16))
        with open("login", "wb") as f2:
            f2.write(data)
        pass


if __name__ == "__main__":
    unittest.main()
