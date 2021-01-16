# -*- coding: utf-8 -*-
"""
from /client/global.go
"""
import random
import hashlib

from pydantic import BaseModel, Field

from pymirai import utils, binary

NumberRange = "0123456789"


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


class Version(BaseModel):
    incremental: bytes
    release: bytes
    code_name: bytes
    sdk: int


class DeviceInfo(BaseModel):
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
    imei: bytes = Field(b"468356291846738")
    android_id: bytes = Field(b"PYMIRAI.123456.001")
    apn: bytes = Field(b"wifi")
    guid: bytes
    tgtgt_key: bytes
    protocol: int = Field(2)
    version: "Version" = Version(incremental=b"5891938",
                                 release=b"10",
                                 code_name=b"REL",
                                 sdk=29)

    def to_json(self) -> str:
        f = DeviceInfoFile(display=self.display,
                           product=self.product,
                           device=self.device,
                           board=self.board,
                           model=self.model,
                           finger_print=self.finger_print,
                           boot_id=self.boot_id,
                           proc_version=self.proc_version,
                           imei=self.imei,
                           protocol=self.protocol
                           )
        return f.json()

    @classmethod
    def read_json(cls, d: str) -> "DeviceInfo":
        f: DeviceInfoFile = DeviceInfoFile.parse_raw(d)
        instance = cls(**f.dict())
        instance.gen_new_guid()
        instance.gen_new_tgtgt_key()
        return instance

    @classmethod
    def gen_new_guid(cls):
        t: bytes = hashlib.md5((cls.android_id + cls.mac_address).encode()).digest()
        cls.__fields__["guid"].default = t

    @classmethod
    def gen_new_tgtgt_key(cls):
        r: bytes = random.randbytes(16)
        t: bytes = hashlib.md5(r + cls.guid).digest()
        cls.__fields__["tgtgt_key"].default = t

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
    DeviceInfo.__fields__["display"].default = ("PYMIRAI" + utils.random_string_range(6, NumberRange) + ".001").encode()
    DeviceInfo.__fields__["finger_print"].default = ("synodriver/pymirai/mirai:10/PYMIRAI.200122.001/"
                                                     + utils.random_string_range(7, NumberRange)
                                                     + ":user/release-keys").encode()
    DeviceInfo.__fields__["boot_id"].default = binary.gen_uuid(r).encode()
    DeviceInfo.__fields__["proc_version"].default = ("Linux version 3.0.31-"
                                                     + utils.random_string(8)
                                                     + " (android-build@xxx.xxx.xxx.xxx.com)")
    r: bytes = random.randbytes(16)
    t: bytes = hashlib.md5(r).digest()
    DeviceInfo.__fields__["imsi_md5"].default = t
    DeviceInfo.__fields__["imei"].default = utils.random_string_range(15, NumberRange)
    DeviceInfo.__fields__["android_id"].default = DeviceInfo.__fields__["display"].default
    DeviceInfo.gen_new_guid()
    DeviceInfo.gen_new_tgtgt_key()


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
        return VersionInfo(apk_id="com.tencent.mobileqq",
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
        return VersionInfo(apk_id="com.tencent.mobileqq",
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


if __name__ == "__main__":
    pass
