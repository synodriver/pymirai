# -*- coding: utf-8 -*-
import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase

from pymirai.signals import SignalManager


class TestPack(IsolatedAsyncioTestCase):
    async def a(self, t):
        await asyncio.sleep(t)
        print(f"收到了a信号 {t}")
        return t

    async def b(self, t):
        await asyncio.sleep(t)
        print(f"收到了b信号 {t}")
        return t

    async def asyncSetUp(self) -> None:
        self.signal = SignalManager()
        self.signal.connect(self.a, "a")
        self.signal.connect(self.b, "b")

    async def test_a(self):
        data = await self.signal.send_async("a", 1)
        self.assertEqual(len(data), 1, "接收到信号的函数个数不正确")
        self.assertEqual(data[0][0], self.a, "错误的函数接收到了信号")
        self.assertEqual(data[0][1], 1, "返回值错误")

    async def test_b(self):
        data = await self.signal.send_async("b", 1)
        self.assertEqual(len(data), 1, "接收到信号的函数个数不正确")
        self.assertEqual(data[0][0], self.b, "错误的函数接收到了信号")
        self.assertEqual(data[0][1], 1, "返回值错误")


if __name__ == "__main__":
    unittest.main()
