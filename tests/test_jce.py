# -*- coding: utf-8 -*-
import unittest

from pymirai.binary.jce import JceReader


class TestJce(unittest.TestCase):
    def test_decode(self):
        # with open("datas", "rb") as f:
        #     data = f.read()
        reader = JceReader(
            b'\x02\x00\x00\x00\x03\x15@\x0effffff&\t\xe5\x93\x88\xe5\x93\x88\xe5\x93\x889\x02\x00\x00\x00\x03\x02\x00\x00\x00\x03\x05@\x0effffff\x06\t\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88H\x02\x00\x00\x00\x02\x06\t\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88\x16\t\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88\x02\x00\x00\x00\x03\x16\t\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88')
        # reader = JceReader(data)
        while True:
            head, _ = reader.peak_head()
            print(reader.read_any(head.tag))
        # self.assertEqual(reader.buffer.position,100)
        pass


def main():
    pass


if __name__ == "__main__":
    main()
