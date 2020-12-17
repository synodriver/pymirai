# -*- coding: utf-8 -*-
"""
from https://github.com/Mrs4s/MiraiGo/blob/94779a6b765bf1acd23bd99fa1cbf1b2ff6fa75a/client/client.go
"""
from pydantic import BaseModel


class Client(BaseModel):
    """
    qq客户端
    """
    uin: int
    password_md5: str
    allow_slider: bool
    nickname:str
    age:int
    gender:int
