# -*- coding: utf-8 -*-
"""
接收到数据的时候广播信号，调用函数来处理  对,我抄了scrapy
"""
import asyncio
from typing import Callable, Any, List, Tuple

from pydispatch import dispatcher


class SignalManager:
    def __init__(self, sender=dispatcher.Anonymous):
        self.sender = sender

    def connect(self, receiver: Callable, signal: Any, **kwargs) -> None:
        """
        注册一个信号的响应函数
        :param receiver: 响应函数
        :param signal: 信号对象
        :param kwargs:
        :return:
        """
        return dispatcher.connect(receiver, signal, self.sender, **kwargs)

    def disconnect(self, receiver: Callable, signal, **kwargs) -> None:
        """
        断开一个接收器的对于给定信号的连接
        :param receiver:
        :param signal:
        :param kwargs:
        :return:
        """
        return dispatcher.disconnect(receiver, signal, self.sender, **kwargs)

    def disconnect_all(self, signal, **kwargs) -> None:
        """
        将所有接收器断开给定信号的连接
        :param signal:
        :param kwargs:
        :return:
        """
        for receiver in dispatcher.liveReceivers(dispatcher.getAllReceivers(self.send, signal)):
            dispatcher.disconnect(receiver, signal, self.sender, **kwargs)

    def send(self, signal, *args, **kwargs) -> List[Tuple]:
        """

        :param signal:
        :param kwargs:
        :return: list of tuple pairs [(receiver, response), ... ]
        """
        kwargs.setdefault('sender', self.sender)
        return dispatcher.send(signal, self.sender, *args, **kwargs)

    async def send_async(self, signal, *args, **kwargs) -> List[Tuple]:
        """
        receiver都是协程的情况下使用
        :param signal:
        :param kwargs:
        :return:  list of tuple pairs [(receiver, response), ... ]
        """

        async def _process_data(data_: List[Tuple]):
            ret = await asyncio.gather(*map(lambda x: x[1], data_))
            return list(zip(map(lambda x: x[0], data_), ret))

        data = dispatcher.send(signal, self.sender, *args, **kwargs)
        return await _process_data(data)
