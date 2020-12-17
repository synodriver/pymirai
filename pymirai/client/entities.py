# -*- coding: utf-8 -*-
"""
from https://github.com/Mrs4s/MiraiGo/blob/94779a6b765bf1acd23bd99fa1cbf1b2ff6fa75a/client/entities.go#L43
"""
from pydantic import BaseModel


class FriendInfo(BaseModel):
    uin: int
    nikename: str
    remark: str
    faceid: int

