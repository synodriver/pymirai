# -*- coding: utf-8 -*-
"""
from https://github.com/Mrs4s/MiraiGo/blob/94779a6b765bf1acd23bd99fa1cbf1b2ff6fa75a/client/client.go
"""
from typing import List
import ipaddress

from pydantic import BaseModel

from pymirai.client.entities import FriendInfo, GroupInfo
from pymirai.client.global_ import VersionInfo
from pymirai.net import TCPConnection
from pymirai.signals import SignalManager


class QQClient(BaseModel):
    """
    qq客户端 sms是短信验证码
    """
    uin: int
    password_md5: str
    allow_slider: bool

    nickname: str
    age: int
    gender: int
    friend_list: List[FriendInfo]
    group_list: List[GroupInfo]
    online: bool
    net_looping: bool

    sequence_id: int
    outgoing_packet_session_id: bytes
    random_key: bytes
    conn: TCPConnection  # tcp连接？
    connect_time: int

    handlers: SignalManager  # 这里跟go不一样 ，用signal订阅发布模式在收到数据后广播信号 ，函数来处理
    servers: List[ipaddress.IPv4Address]
    curr_server_index: int
    retry_times: int
    version: VersionInfo

    sync_cookie: bytes
    pub_account_cookie: bytes
    msg_ctrl_buf: bytes
    ksid: bytes  # 登录包
    t104: bytes
    t174: bytes
    t402: bytes
    t150: bytes
    t149: bytes
    t528: bytes
    t530: bytes
    rollback_sig: bytes
    time_diff: int
    sig_info: "LoginSigInfo"  # TODO 抄go的
    pwd_flag: bool
    last_message_seq: int


class LoginSigInfo(BaseModel):
    pass
