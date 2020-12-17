# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from pymirai.utils.tools import *
from pymirai.utils.tea import Tea


class TestPack(TestCase):

    def test_pack(self):
        a = bytes2hex(Tea.encrypt(str2bytes('哈哈哈'), hex2bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
        # print(a)
        b = bytes2hex(Tea.decrypt(hex2bytes(a), hex2bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
        self.assertEqual(hex2str(b), "哈哈哈")

    def test_decode(self):
        with open("data.txt") as f:
            a = f.read().strip()
        data = Tea.decrypt((hex2bytes(a)), hex2bytes("00 00 00 00 00 00 00 00"))
        pass


if __name__ == "__main__":
    unittest.main()
