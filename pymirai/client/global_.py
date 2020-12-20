# -*- coding: utf-8 -*-
"""
from /client/global.go
"""
from pydantic import BaseModel


class DeviceInfo(BaseModel):
    display: bytes
    product: bytes
    device: bytes
    board: bytes
    brand: bytes
    model: bytes
    boot_loader: bytes
    finger_print: bytes
    boot_id: bytes
    proc_version: bytes
    base_band: bytes
    sim_info: bytes
    os_type: bytes
    mac_address: bytes
    ipaddress: bytes
    wifi_bssid: bytes
    wifi_ssid: bytes
    imsi_md5: bytes
    imei: str
    android_id: bytes
    apn: bytes
    guid: bytes
    tgtgt_key: bytes
    protocol: int
    version: "Version"


class Version(BaseModel):
    incremental: bytes
    release: bytes
    code_name: bytes
    sdk: int


class DeviceInfoFile(BaseModel):
    display: str
    product: str
    device: str
    board: str
    model: str
    fingerprint: str
    boot_id: str
    proc_version: str
    protocol: int  # 0: Pad 1: Phone 2: Watch 3: Mac
    imei: str


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

