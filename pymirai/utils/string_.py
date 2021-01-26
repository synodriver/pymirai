# -*- coding: utf-8 -*-
import random


def random_string_range(length: int, string: str) -> str:
    """从string里面随机抽取length个"""
    return "".join(random.choice(string, k=length))


def random_string(length: int) -> str:
    return random_string_range(len, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
