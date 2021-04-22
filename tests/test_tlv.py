# -*- coding: utf-8 -*-
import sys

from pymirai import binary


def decode(data: bytes):
    reader = binary.Reader(data)
    md5: bytes = reader.read_bytes(16)
    size = reader.read_int32()
    name = reader.read_string()
    url = reader.read_string()
    return md5, size, name, url


def main():
    name: str = sys.argv[1]
    with open(name, "rb") as f:
        data = f.read()
    md5, size, name, url=decode(data)
    print(f"md5:{md5}\nsize:{size}\nname:{name}\nurl:{url}")


if __name__ == "__main__":
    main()
