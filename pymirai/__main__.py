# -*- coding: utf-8 -*-
import os

from pydantic import BaseSettings

from .log import logger


class Device(BaseSettings):
    """
    read from device.json
    """
    display: str
    product: str
    device: str
    board: str
    model: str
    finger_print: str
    boot_id: str
    proc_version: str
    protocol: int = 0
    imei: str


def run():
    """pymirai的入口函数"""
    if not os.path.exists("device.json"):
        logger.debug("Can't find device.json. Will Generate new one")
    pass
