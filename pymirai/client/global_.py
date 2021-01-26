# -*- coding: utf-8 -*-
"""
from /client/global.go
里面放全局变量 一个实例只能存在一份
"""
import random
import hashlib
import threading
from typing import List

from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass

import pyjce
import pymirai.binary.jce as jce

from pymirai import utils, binary

try:
    from pytea import TEA  # C写的
except ImportError:
    from pymirai.binary.tea import TEA  # py写的

NumberRange = "0123456789"


class SingletonType(ModelMetaclass):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:  # 加锁
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class DeviceInfoFile(BaseModel):
    display: str = Field(alias="display")
    product: str = Field(alias="product")
    device: str = Field(alias="device")
    board: str = Field(alias="board")
    model: str = Field(alias="model")
    fingerprint: str = Field(alias="finger_print")
    boot_id: str = Field(alias="boot_id")
    proc_version: str = Field(alias="proc_version")
    protocol: int = Field(alias="protocol")  # 0: Pad 1: Phone 2: Watch 3: Mac
    imei: str = Field(alias="imei")
    brand: str
    bootloader: str
    base_band: str
    version: str
    sim_info: str
    os_type: str
    mac_address: str
    ipaddress: str
    wifi_bssid: str
    wifi_ssid: str
    imsi_md5: str
    android_id: str
    apn: str


class Version(BaseModel):
    incremental: bytes
    release: bytes
    code_name: bytes
    sdk: int


class DeviceInfo(BaseModel, metaclass=SingletonType):
    """
    里面写入默认值 当成全局变量
    """
    display: bytes = Field(b"PYMIRAI.123456.001")
    product: bytes = Field(b"pymirai")
    device: bytes = Field(b"pymirai")
    board: bytes = Field(b"pymirai")
    brand: bytes = Field(b"cpython")
    model: bytes = Field(b"pymirai")
    boot_loader: bytes = Field(b"unknown")
    finger_print: bytes = Field(b"synodriver/pymirai/mirai:10/PYMIRAI.200122.001/1234567:user/release-keys")
    boot_id: bytes = Field(b"cb886ae2-00b6-4d68-a230-787f111d12c7")
    proc_version: bytes = Field(b"Linux version 3.0.31-cb886ae2 (android-build@xxx.xxx.xxx.xxx.com)")
    base_band: bytes = Field(b"")
    sim_info: bytes = Field(b"T-Mobile")
    os_type: bytes = Field(b"android")
    mac_address: bytes = Field(b"00:50:56:C0:00:08")
    ipaddress: bytes = Field(bytes([10, 0, 1, 3]))
    wifi_bssid: bytes = Field(b"00:50:56:C0:00:08")
    wifi_ssid: bytes = Field(b"<unknown ssid>")
    imsi_md5: bytes = Field(hashlib.md5(utils.randbytes(16)).digest())
    imei: str = Field("468356291846738")
    android_id: bytes = Field(b"PYMIRAI.123456.001")
    apn: bytes = Field(b"wifi")
    guid: bytes = Field(None)
    tgtgt_key: bytes = Field(None)
    protocol: int = Field(2)
    version: "Version" = Version(incremental=b"5891938",
                                 release=b"10",
                                 code_name=b"REL",
                                 sdk=29)

    # def to_json(self) -> str:
    # f = DeviceInfoFile(display=self.display,
    #                    product=self.product,
    #                    device=self.device,
    #                    board=self.board,
    #                    model=self.model,
    #                    finger_print=self.finger_print,
    #                    boot_id=self.boot_id,
    #                    proc_version=self.proc_version,
    #                    imei=self.imei,
    #
    #                    protocol=self.protocol
    #                    )
    # return self.json()

    @classmethod
    def read_json(cls, d: str) -> "DeviceInfo":
        instance: DeviceInfo = cls.parse_raw(d)
        instance.gen_new_guid()
        instance.gen_new_tgtgt_key()
        return instance

    def gen_new_guid(self):
        t: bytes = hashlib.md5((self.android_id + self.mac_address).encode()).digest()
        self.guid = t

    def gen_new_tgtgt_key(self):
        r: bytes = random.randbytes(16)
        t: bytes = hashlib.md5(r + self.guid).digest()
        self.tgtgt_key = t

    def gen_device_info_data(self):
        # todo 这个需要pb
        pass


class GroupMessageBuilder(BaseModel):
    """
    TODO 留给pb
    """


class VersionInfo(BaseModel):
    apk_sign: bytes
    apk_id: str
    sort_version_name: str
    sdk_version: str
    app_id: int
    build_time: int
    sso_version: int
    misc_bitmap: int
    sub_sigmap: int
    main_sigmap: int


def gen_random_device():
    """
    生成随机设备信息
    :return:
    """
    r: bytes = random.randbytes(16)
    instance = DeviceInfo()
    instance.display = ("PYMIRAI" + utils.random_string_range(6, NumberRange) + ".001").encode()
    instance.finger_print = ("synodriver/pymirai/mirai:10/PYMIRAI.200122.001/"
                             + utils.random_string_range(7, NumberRange)
                             + ":user/release-keys").encode()
    instance.boot_id = binary.gen_uuid(r).encode()
    instance.proc_version = ("Linux version 3.0.31-"
                             + utils.random_string(8)
                             + " (android-build@xxx.xxx.xxx.xxx.com)")
    r: bytes = random.randbytes(16)
    t: bytes = hashlib.md5(r).digest()
    instance.imsi_md5 = t
    instance.imei = utils.random_string_range(15, NumberRange)
    instance.android_id = instance.display
    instance.gen_new_guid()
    instance.gen_new_tgtgt_key()


def get_version_info(p: int) -> VersionInfo:
    if p == 1:  # AndroidPhone: Dumped by mirai from qq android v8.2.7
        return VersionInfo(apk_id="com.tencent.mobileqq",
                           app_id=537066738,
                           sort_version_name="8.5.0",
                           build_time=1607689988,
                           apk_sign=bytes(
                               [0xA6, 0xB7, 0x45, 0xBF, 0x24, 0xA2, 0xC2, 0x77, 0x52, 0x77, 0x16, 0xF6, 0xF3, 0x6E,
                                0xB6, 0x8D]),
                           sdk_version="6.0.0.2454",
                           sso_version=15,
                           misc_bitmap=184024956,
                           sub_sigmap=0x10400,
                           main_sigmap=34869472)
    elif p == 2:  # IPad
        return VersionInfo(apk_id="com.tencent.minihd.qq",
                           app_id=537065739,
                           sort_version_name="5.8.9",
                           build_time=1595836208,
                           apk_sign=bytes(
                               [170, 57, 120, 244, 31, 217, 111, 249, 145, 74, 102, 158, 24, 100, 116, 199]),
                           sdk_version="6.0.0.2433",
                           sso_version=12,
                           misc_bitmap=150470524,
                           sub_sigmap=66560,
                           main_sigmap=1970400)
    elif p == 3:  # AndroidWatch
        return VersionInfo(apk_id="com.tencent.mobileqq",
                           app_id=537061176,
                           sort_version_name="8.2.7",
                           build_time=1571193922,
                           apk_sign=bytes(
                               [0xA6, 0xB7, 0x45, 0xBF, 0x24, 0xA2, 0xC2, 0x77, 0x52, 0x77, 0x16, 0xF6, 0xF3, 0x6E,
                                0xB6, 0x8D]),
                           sdk_version="6.0.0.2413",
                           sso_version=5,
                           misc_bitmap=184024956,
                           sub_sigmap=0x10400,
                           main_sigmap=34869472)
    elif p == 4:  # MacOS:
        return VersionInfo(apk_id="com.tencent.minihd.qq",
                           app_id=537064315,
                           sort_version_name="5.8.9",
                           build_time=1595836208,
                           apk_sign=bytes(
                               [170, 57, 120, 244, 31, 217, 111, 249, 145, 74, 102, 158, 24, 100, 116, 199]),
                           sdk_version="6.0.0.2433",
                           sso_version=12,
                           misc_bitmap=150470524,
                           sub_sigmap=66560,
                           main_sigmap=1970400)


def gen_imei() -> str:
    final = ""
    sum_: int = 0
    for i in range(14):
        to_add = random.randint(0, 9)
        if (i + 1) % 2 == 0:
            to_add *= 2
            if to_add > 10:
                to_add = (to_add % 10) + 1
        sum_ += to_add
        final += str(to_add)
    ctrl_digit = (sum_ * 9) % 10
    final += str(ctrl_digit)
    return final


def pack_uni_request_data(data: bytes):
    r = bytes([0x0A]) + data + bytes([0x0B])
    return r


async def get_sso_address():
    protocol: VersionInfo = get_version_info(DeviceInfo().protocol)
    key: bytes = bytes.fromhex("F0441F5FF42DA58FDCF7949ABA62D411")
    payload = pyjce.JceWriter().write_int64(0, 1).write_int64(0, 2).write_byte(bytes([1]), 3) \
        .write_string("00000", 4).write_int32(100, 5).write_int32(protocol.app_id, 6).write_string(DeviceInfo().imei, 7) \
        .write_int64(0, 8).write_int64(0, 9).write_int64(0, 10).write_int64(0, 11).write_byte(bytes([0]), 12) \
        .write_int64(0, 13).write_byte(bytes([1]), 14).bytes()
    buf = jce.RequestDataVersion2(
        map={"HttpServerListReq": {"ConfigHttp.HttpServerListReq": pack_uni_request_data(payload)}})
    pkt = jce.RequestPacket(iversion=2, sservant_name="ConfigHttp", sfunc_name="HttpServerListReq",
                            sbuffer=buf.to_bytes())

    tea = TEA(key)
    writer = binary.Writer()
    writer.write_int_lv_packet(0, lambda w: w.write(pkt.to_bytes()))
    post_bytes = tea.encrypt(bytes(writer.bytes()))
    resp = await utils.http_post_bytes("https://configsvr.msf.3g.qq.com/configsvr/serverlist.jsp", post_bytes)
    resp_pkt = jce.RequestPacket()
    data = jce.RequestDataVersion2()
    resp_pkt.read_from(pyjce.JceReader(tea.decrypt(resp)[4:]))
    data.read_from(pyjce.JceReader(resp_pkt.sbuffer))
    reader = pyjce.JceReader(data.map["HttpServerListRes"]["ConfigHttp.HttpServerListRes"][1:])
    servers: List[jce.SsoServerInfo] = reader.read_list(jce.SsoServerInfo, 2)

    add = []
    for server in servers:
        if "com" in server.server:
            continue
        add.append(server)
    return add


if __name__ == "__main__":
    # print(gen_imei())

    import asyncio

    data = asyncio.run(get_sso_address())
    print(data)
