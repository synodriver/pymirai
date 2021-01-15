# -*- coding: utf-8 -*-
"""
from /client/global.go
"""
import random
import hashlib

from pydantic import BaseModel, Field


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
    display: str = "PYMIRAI.123456.001"
    product: str = "pymirai"
    device: str = "pymirai"
    board: str = "pymirai"
    brand: str = "cpython"
    model: str = "pymirai"
    boot_loader: str = "unknown"
    finger_print: str = "synodriver/pymirai/mirai:10/PYMIRAI.200122.001/1234567:user/release-keys"
    boot_id: str = "cb886ae2-00b6-4d68-a230-787f111d12c7"
    proc_version: str = "Linux version 3.0.31-cb886ae2 (android-build@xxx.xxx.xxx.xxx.com)"
    base_band: str = ""
    sim_info: str = "T-Mobile"
    os_type: str = "android"
    mac_address: str = "00:50:56:C0:00:08"
    ipaddress: bytes = bytes([10, 0, 1, 3])
    wifi_bssid: str = "00:50:56:C0:00:08"
    wifi_ssid: str = "<unknown ssid>"
    imsi_md5: bytes = hashlib.md5(random.randbytes(16)).digest()
    imei: str = "468356291846738"
    android_id: str = "PYMIRAI.123456.001"
    apn: str = "wifi"
    guid: bytes
    tgtgt_key: bytes
    protocol: int = 2
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
