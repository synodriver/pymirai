# -*- coding: utf-8 -*-
"""
from https://github.com/Mrs4s/MiraiGo/blob/94779a6b765bf1acd23bd99fa1cbf1b2ff6fa75a/client/entities.go#L43
"""
import asyncio
from typing import List

from pydantic import BaseModel

from .client import QQClient

NeedCaptcha = 1
OtherLoginError = 3
UnsafeDeviceError = 4
SMSNeededError = 5
TooManySMSRequestError = 6
SMSOrVerifyNeededError = 7
SliderNeededError = 8
UnknownLoginError = -1

Owner = 0
Administrator = 1
Member = 2

AndroidPhone = 1
IPad = 2
AndroidWatch = 3
MacOS = 4


class LoginResponse(BaseModel):
    success: bool
    error: int
    # Captcha info
    captcha_image: bytes
    captcha_sign: bytes
    # Unsafe device
    verify_url: str
    # SMS needed
    sms_phone: str
    # other error
    error_message: str


class FriendInfo(BaseModel):
    uin: int
    nike_name: str
    remark: str
    face_id: int


class FriendListResponse(BaseModel):
    total_count: int
    list_: List[FriendInfo]


class SummaryCardInfo(BaseModel):
    uin: int
    sex: bytes
    age: int
    nick_name: str
    level: int
    city: str
    sign: str
    mobile: str
    login_days: int


class GroupInfo(BaseModel):
    uin: int
    code: int
    name: str
    memo: str
    owner_uin: int
    member_count: int
    max_member_count: int
    members: List["GroupMemberInfo"]
    client: QQClient
    last_msg_seq: int
    lock: asyncio.Lock  # 我们为什么要锁?我们是高贵的py,有gil的  昵昵说，消息异步处理，可能修改members，因此要加读写锁.那就加上吧


class GroupMemberInfo(BaseModel):
    group: GroupInfo
    uin: int
    gender: bytes
    nick_name: str
    card_name: str
    level: int
    join_time: int
    last_speak_time: int
    special_title: str
    special_title_expire_time: int  # 震惊:特殊头衔居然会过期
    permission: int  # go里面是MemberPermission int  emmm 要不变枚举?


class GroupMuteEvent(BaseModel):
    group_code: int
    operator_uin: int
    target_uin: int
    time: int


class GroupMessageRecalledEvent(BaseModel):
    group_code: int
    operator_uin: int
    author_uin: int
    message_id: int
    time: int


class FriendMessageRecalledEvent(BaseModel):
    friend_uin: int
    message_id: int
    time: int


class GroupLeaveEvent(BaseModel):
    group: GroupInfo
    operator: GroupMemberInfo


class MemberJoinGroupEvent(BaseModel):
    group: GroupInfo
    member: GroupMemberInfo


class MemberCardUpdatedEvent(BaseModel):
    group: GroupInfo
    old_card: str
    member: GroupMemberInfo


# TODO 这里有个接口 暂时作用不明确

class MemberLeaveGroupEvent(BaseModel):
    group: GroupInfo
    member: GroupMemberInfo
    operator: GroupMemberInfo


class MemberPermissionChangedEvent(BaseModel):
    group: GroupInfo
    member: GroupMemberInfo
    old_permission: int
    new_permission: int


class ClientDisconnectedEvent(BaseModel):
    message: str


class NewFriendRequest(BaseModel):
    request_id: int
    message: str
    requester_uin: int
    requester_nick: int
    client: QQClient


class LogEvent(BaseModel):
    type_: str
    message: str


class ServerUpdatedEvent(BaseModel):
    """
    服务器ip换了   TODO 抄这个得看pb了先放放
    """
    pass


class NewFriendEvent(BaseModel):
    friend: FriendInfo


class OfflineFileEvent(BaseModel):
    file_name: str
    file_size: int
    sender: int
    download_url: str


class OcrResponse(BaseModel):
    texts: List["TextDetection"]  # TODO 看go的ocr实现
    language: str


class TextDetection(BaseModel):
    text: str
    confidence: int
    coordinates: List["Coordinate"]  # 坐标


class Coordinate(BaseModel):
    x: int
    y: int


class GroupMemberListResponse(BaseModel):
    next_uin: int
    list_: List[GroupMemberInfo]


class ImageUploadResponse(BaseModel):
    pass

# TODO 抄到206了 不写了
