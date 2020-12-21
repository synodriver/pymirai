# -*- coding: utf-8 -*-
import unittest

from pymirai.binary.jce import JceReader


class TestJce(unittest.TestCase):
    def test_decode(self):
        with open("datas", "rb") as f:
            data = f.read()
        reader = JceReader(data)

        while True:
            head, _ = reader.peak_head()
            print(reader.read_any(head.tag))



        pass


def main():
    pass


if __name__ == "__main__":
    main()
