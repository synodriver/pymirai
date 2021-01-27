# -*- coding: utf-8 -*-
from typing import Dict, List, Union

from pydantic import BaseModel, Field
from pyjce import JceReader, JceWriter, IJceStruct


class RequestPacket(IJceStruct):  # todo 加入jceid标注
    iversion: int = Field(0, jce_id=1)  # int16   `jceId:"1"`
    cpacket_type: Union[bytes, bytearray] = Field(bytes([0]), jce_id=2)  # byte              `jceId:"2"`
    imessage_type: int = Field(0, jce_id=3)  # int32             `jceId:"3"`
    irequest_id: int = Field(0, jce_id=4)  # int32             `jceId:"4"`
    sservant_name: str = Field("", jce_id=5)  # string            `jceId:"5"`
    sfunc_name: str = Field("", jce_id=6)  # string            `jceId:"6"`
    sbuffer: Union[bytes, bytearray] = Field(bytes([0]), jce_id=7)  # []byte            `jceId:"7"`
    itimeout: int = Field(0, jce_id=8)  # int32             `jceId:"8"`
    context: Dict[str, str] = Field({}, jce_id=9)  # map[string]string `jceId:"9"`
    status: Dict[str, str] = Field({}, jce_id=10)  # map[string]string `jceId:"10"`

    def to_bytes(self) -> bytearray:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    def read_from(self, reader: JceReader):
        self.iversion = reader.read_int16(1)
        self.cpacket_type = reader.read_byte(2)
        self.imessage_type = reader.read_int32(3)
        self.irequest_id = reader.read_int32(4)
        self.sservant_name = reader.read_string(5)
        self.sfunc_name = reader.read_string(6)
        self.sbuffer = reader.read_any(7)
        self.itimeout = reader.read_int32(8)
        self.context = reader.read_any(9)
        self.status = reader.read_any(10)

    class Config:
        arbitrary_types_allowed = True


class RequestDataVersion3(IJceStruct):
    map: Dict[str, bytes] = Field(None, jce_id=0)  # map[string]map[string][]byte `jceId:"0"`

    def to_bytes(self) -> bytearray:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    def read_from(self, reader: JceReader):
        self.map = reader.read_any(0)


class RequestDataVersion2(IJceStruct):
    map: Dict[str, Dict[str, bytes]] = Field(None, jce_id=0)

    def to_bytes(self) -> bytearray:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    def read_from(self, reader: JceReader):
        self.map = reader.read_any(0)


class SsoServerInfo(IJceStruct):
    server: str = Field(None, jce_id=1)  # string `jceId:"1"`
    port: int = Field(None, jce_id=2)  # int32  `jceId:"2"`
    location: str = Field(None, jce_id=8)  # string `jceId:"8"`

    def read_from(self, reader: JceReader):
        self.server = reader.read_string(1)
        self.port = reader.read_int32(2)
        self.location = reader.read_string(8)

    def to_bytes(self) -> Union[bytes, bytearray]:
        pass


class BigDataIPInfo(IJceStruct):
    type_: int  # int64  `jceId:"0"`
    server: str  # string `jceId:"1"`
    port: int  # int64  `jceId:"2"`

    def read_from(self, reader: JceReader):
        self.type_ = reader.read_int64(0)
        self.server = reader.read_string(1)
        self.port = reader.read_int64(2)

    def to_bytes(self) -> Union[bytes, bytearray]:
        pass


class BigDataIPList(IJceStruct):
    service_type: int  # int64           `jceId:"0"`
    ip_list: List[BigDataIPInfo]  # []BigDataIPInfo `jceId:"1"`
    fragment_size: int  # int64           `jceId:"3"`

    def read_from(self, reader: JceReader):
        self.service_type = reader.read_int64(0)
        self.ip_list = reader.read_list(BigDataIPInfo, 1)
        self.fragment_size = reader.read_int64(2)

    def to_bytes(self) -> Union[bytes, bytearray]:
        pass


class BigDataChannel(IJceStruct):
    ip_lists: List[BigDataIPList]  # []BigDataIPList `jceId:"0"`
    sig_session: bytes  # []byte          `jceId:"1"`
    key_session: bytes  # []byte          `jceId:"2"`
    sig_uin: int  # int64           `jceId:"3"`
    connect_flag: int  # int32           `jceId:"4"`
    pb_buf: bytes  # []byte          `jceId:"5"`

    def read_from(self, reader: JceReader):
        self.ip_lists = reader.read_list(BigDataIPList, 0)
        self.sig_session = reader.read_any(1)
        self.key_session = reader.read_any(2)
        self.sig_uin = reader.read_int64(3)
        self.connect_flag = reader.read_int32(4)
        self.pb_buf = reader.read_any(5)

    def to_bytes(self) -> Union[bytes, bytearray]:
        pass


class FileStorageServerInfo(IJceStruct):
    server: str = Field(None, jce_id=1)  # `jceid:"1"`
    port: int = Field(None, jce_id=2)  # jceId:"2"`

    def read_from(self, reader: JceReader):
        self.server = reader.read_string(1)
        self.port = reader.read_int32(2)

    def to_bytes(self) -> Union[bytes, bytearray]:
        pass


class FileStoragePushFSSvcList(IJceStruct):
    upload_list: List[FileStorageServerInfo] = Field(None, jce_id=0)  # []FileStorageServerInfo `jceId:"0"`
    pic_download_list: List[FileStorageServerInfo] = Field(None, jce_id=1)  # []FileStorageServerInfo `jceId:"1"`
    gpic_download_list: List[FileStorageServerInfo] = Field(None, jce_id=2)  # []FileStorageServerInfo `jceId:"2"`
    qzone_proxy_service_list: List[FileStorageServerInfo] = Field(None, jce_id=3)  # []FileStorageServerInfo `jceId:"3"`
    url_encode_service_list: List[FileStorageServerInfo] = Field(None, jce_id=4)  # []FileStorageServerInfo `jceId:"4"`
    big_data_channel: "BigDataChannel" = Field(None, jce_id=5)  # *BigDataChannel         `jceId:"5"`
    vip_emotion_list: List[FileStorageServerInfo] = Field(None, jce_id=6)  # []FileStorageServerInfo `jceId:"6"`
    c2c_pic_down_list: List[FileStorageServerInfo] = Field(None, jce_id=7)  # []FileStorageServerInfo `jceId:"7"`
    # FmtIPInfo          #   *FmtIPInfo `jceId:"8"`
    # DomainIPChannel    #   *DomainIPChannel `jceId:"9"`
    ptt_list: bytes = Field(None, jce_id=10)  # []byte `jceId:"10"`

    def read_from(self, reader: JceReader):
        self.upload_list = reader.read_list(FileStorageServerInfo, 0)
        self.pic_download_list = reader.read_list(FileStorageServerInfo, 1)
        self.gpic_download_list = reader.read_list(FileStorageServerInfo, 2)
        self.qzone_proxy_service_list = reader.read_list(FileStorageServerInfo, 3)
        self.url_encode_service_list = reader.read_list(FileStorageServerInfo, 4)
        self.big_data_channel = reader.read_object(BigDataChannel)
        self.vip_emotion_list = reader.read_list(FileStorageServerInfo, 6)
        self.c2c_pic_down_list = reader.read_list(FileStorageServerInfo, 7)
        self.ptt_list = reader.read_any(10)
        pass


class SvcReqRegister(BaseModel):
    uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    bid: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    conn_type: Union[bytes, bytearray] = Field(None, jce_id=2)  # byte   `jceId:"2"`
    other: str = Field(None, jce_id=3)  # string `jceId:"3"`
    status: int = Field(None, jce_id=4)  # int32  `jceId:"4"`
    online_push: Union[bytes, bytearray] = Field(None, jce_id=5)  # byte   `jceId:"5"`
    is_online: Union[bytes, bytearray] = Field(None, jce_id=6)  # byte   `jceId:"6"`
    is_show_online: Union[bytes, bytearray] = Field(None, jce_id=7)  # byte   `jceId:"7"`
    kick_pc: Union[bytes, bytearray] = Field(None, jce_id=8)  # byte   `jceId:"8"`
    kick_weak: Union[bytes, bytearray] = Field(None, jce_id=9)  # byte   `jceId:"9"`
    time_stamp: int = Field(None, jce_id=10)  # int64  `jceId:"10"`
    ios_version: int = Field(None, jce_id=11)  # int64  `jceId:"11"`
    net_type: Union[bytes, bytearray] = Field(None, jce_id=12)  # byte   `jceId:"12"`
    build_ver: str = Field(None, jce_id=13)  # string `jceId:"13"`
    reg_type: Union[bytes, bytearray] = Field(None, jce_id=14)  # byte   `jceId:"14"`
    dev_param: Union[bytes, bytearray] = Field(None, jce_id=15)  # []byte `jceId:"15"`
    guid: Union[bytes, bytearray] = Field(None, jce_id=16)  # []byte `jceId:"16"`
    locale_id: int = Field(None, jce_id=17)  # int32  `jceId:"17"`
    silent_push: Union[bytes, bytearray] = Field(None, jce_id=18)  # byte   `jceId:"18"`
    dev_name: str = Field(None, jce_id=19)  # string `jceId:"19"`
    dev_type: str = Field(None, jce_id=20)  # string `jceId:"20"`
    os_ver: str = Field(None, jce_id=21)  # string `jceId:"21"`
    open_push: Union[bytes, bytearray] = Field(None, jce_id=22)  # byte   `jceId:"22"`
    large_seq: int = Field(None, jce_id=23)  # int64  `jceId:"23"`
    last_watch_start_time: int = Field(None, jce_id=24)  # int64  `jceId:"24"`
    old_sso_ip: int = Field(None, jce_id=26)  # int64  `jceId:"26"`
    new_sso_ip: int = Field(None, jce_id=27)  # int64  `jceId:"27"`
    channel_no: str = Field(None, jce_id=28)  # string `jceId:"28"`
    cp_id: int = Field(None, jce_id=29)  # int64  `jceId:"29"`
    vendor_name: str = Field(None, jce_id=30)  # string `jceId:"30"`
    vendor_osname: str = Field(None, jce_id=31)  # string `jceId:"31"`
    ios_idfa: str = Field(None, jce_id=32)  # string `jceId:"32"`
    b769: Union[bytes, bytearray] = Field(None, jce_id=33)  # []byte `jceId:"33"`
    is_set_status: Union[bytes, bytearray] = Field(None, jce_id=34)  # byte   `jceId:"34"`
    server_buf: Union[bytes, bytearray] = Field(None, jce_id=35)  # []byte `jceId:"35"`
    set_mute: Union[bytes, bytearray] = Field(None, jce_id=36)  # byte   `jceId:"36"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class SvcRespRegister(IJceStruct):
    uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    bid: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    reply_code: Union[bytes, bytearray] = Field(None, jce_id=2)  # byte   `jceId:"2"`
    result: str = Field(None, jce_id=3)  # string `jceId:"3"`
    server_time: int = Field(None, jce_id=4)  # int64  `jceId:"4"`
    log_qq: Union[bytes, bytearray] = Field(None, jce_id=5)  # byte   `jceId:"5"`
    need_kik: Union[bytes, bytearray] = Field(None, jce_id=6)  # byte   `jceId:"6"`
    update_flag: Union[bytes, bytearray] = Field(None, jce_id=7)  # byte   `jceId:"7"`
    timestamp: int = Field(None, jce_id=8)  # int64  `jceId:"8"`
    crash_flag: Union[bytes, bytearray] = Field(None, jce_id=9)  # byte   `jceId:"9"`
    client_ip: str = Field(None, jce_id=10)  # string `jceId:"10"`
    client_port: int = Field(None, jce_id=11)  # int32  `jceId:"11"`
    hello_interval: int = Field(None, jce_id=12)  # int32  `jceId:"12"`
    large_seq: int = Field(None, jce_id=13)  # int32  `jceId:"13"`
    large_seq_update: Union[bytes, bytearray] = Field(None, jce_id=14)  # byte   `jceId:"14"`
    d769_rsp_body: Union[bytes, bytearray] = Field(None, jce_id=15)  # []byte `jceId:"15"`
    status: int = Field(None, jce_id=16)  # int32  `jceId:"16"`
    ext_online_status: int = Field(None, jce_id=17)  # int64  `jceId:"17"`
    client_battery_get_interval: int = Field(None, jce_id=18)  # int64  `jceId:"18"`
    client_auto_status_interval: int = Field(None, jce_id=19)  # int64  `jceId:"19"`

    def read_from(self, reader: JceReader):
        self.uin = reader.read_int64(0)
        self.bid = reader.read_int64(1)
        self.reply_code = reader.read_byte(2)
        self.result = reader.read_string(3)
        self.server_time = reader.read_int64(4)
        self.log_qq = reader.read_byte(5)
        self.need_kik = reader.read_byte(6)
        self.update_flag = reader.read_byte(7)
        self.timestamp = reader.read_int64(8)
        self.crash_flag = reader.read_byte(9)
        self.client_ip = reader.read_string(10)
        self.client_port = reader.read_int32(11)
        self.hello_interval = reader.read_int32(12)
        self.large_seq = reader.read_int32(13)
        self.large_seq_update = reader.read_byte(14)
        self.d769_rsp_body = reader.read_any(15)
        self.status = reader.read_int32(16)
        self.ext_online_status = reader.read_int64(17)
        self.client_battery_get_interval = reader.read_int64(18)
        self.client_auto_status_interval = reader.read_int64(19)

    class Config:
        arbitrary_types_allowed = True


class PushMessageInfo(IJceStruct):
    """昵昵说不连续的jce是因为不需要那些 如广告"""
    from_uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    msg_time: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    msg_type: int = Field(None, jce_id=2)  # int16  `jceId:"2"`
    msg_seq: int = Field(None, jce_id=3)  # int16  `jceId:"3"`
    msg: str = Field(None, jce_id=4)  # string `jceId:"4"`
    real_msg_time: int = Field(None, jce_id=5)  # int32  `jceId:"5"`
    vmsg: Union[bytes, bytearray] = Field(None, jce_id=6)  # []byte `jceId:"6"`
    app_share_id: int = Field(None, jce_id=7)  # int64  `jceId:"7"`
    msg_cookies: Union[bytes, bytearray] = Field(None, jce_id=8)  # []byte `jceId:"8"`
    app_share_cookie: Union[bytes, bytearray] = Field(None, jce_id=9)  # []byte `jceId:"9"`
    msg_uid: int = Field(None, jce_id=10)  # int64  `jceId:"10"`
    last_change_time: int = Field(None, jce_id=11)  # int64  `jceId:"11"`
    from_inst_id: int = Field(None, jce_id=14)  # int64  `jceId:"14"`
    remark_of_sender: Union[bytes, bytearray] = Field(None, jce_id=15)  # []byte `jceId:"15"`
    from_mobile: str = Field(None, jce_id=16)  # string `jceId:"16"`
    from_name: str = Field(None, jce_id=17)  # string `jceId:"17"`

    def read_from(self, reader: JceReader):
        self.from_uin = reader.read_int64(0)
        self.msg_time = reader.read_int64(1)
        self.msg_type = reader.read_int16(2)
        self.msg_seq = reader.read_int16(3)
        self.msg = reader.read_string(4)
        self.real_msg_time = reader.read_int32(5)
        self.vmsg = reader.read_any(6)
        self.app_share_id = reader.read_int64(7)
        self.msg_cookies = reader.read_any(8)
        self.app_share_cookie = reader.read_any(9)
        self.msg_uid = reader.read_int64(10)
        self.last_change_time = reader.read_int64(11)
        self.from_inst_id = reader.read_int64(14)
        self.remark_of_sender = reader.read_any(15)
        self.from_mobile = reader.read_string(16)
        self.from_name = reader.read_string(17)

    class Config:
        arbitrary_types_allowed = True


class SvcRespPushMsg(BaseModel):
    uin: int = Field(None, jce_id=0)  # int64        `jceId:"0"`
    del_infos: List[IJceStruct] = Field(None, jce_id=1)  # []IJceStruct `jceId:"1"`
    svr_ip: int = Field(None, jce_id=2)  # int32        `jceId:"2"`
    push_token: Union[bytes, bytearray] = Field(None, jce_id=3)  # []byte       `jceId:"3"`
    service_type: int = Field(None, jce_id=4)  # int32        `jceId:"4"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class SvcReqGetDevLoginInfo(BaseModel):
    guid: Union[bytes, bytearray] = Field(None, jce_id=0)  # []byte `jceId:"0"`
    app_name: str = Field(None, jce_id=1)  # string `jceId:"1"`
    login_type: int = Field(None, jce_id=2)  # int64  `jceId:"2"`
    time_stamp: int = Field(None, jce_id=3)  # int64  `jceId:"3"`
    next_item_index: int = Field(None, jce_id=4)  # int64  `jceId:"4"`
    require_max: int = Field(None, jce_id=5)  # int64  `jceId:"5"`
    get_dev_list_type: int = Field(None,
                                   jce_id=6)  # int64  1: getLoginDevList 2: getRecentLoginDevList 4:

    # getAuthLoginDevList

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class SvcDevLoginInfo(IJceStruct):
    app_id: int  # int64
    guid: Union[bytes, bytearray]  # []byte
    login_time: int  # int64
    login_platform: int  # int64
    login_location: str  # string
    device_name: str  # string
    device_type_info: str  # string
    ter_type: int  # int64
    product_type: int  # int64
    can_be_kicked: int  # int64

    def read_from(self, reader: JceReader):
        self.app_id = reader.read_int64(0)
        self.guid = reader.read_any(1)
        self.login_time = reader.read_int64(2)
        self.login_platform = reader.read_int64(3)
        self.login_location = reader.read_string(4)
        self.device_name = reader.read_string(5)
        self.device_type_info = reader.read_string(6)
        self.ter_type = reader.read_int64(8)
        self.product_type = reader.read_int64(9)
        self.can_be_kicked = reader.read_int64(10)

    class Config:
        arbitrary_types_allowed = True


class DelMsgInfo(BaseModel):
    from_uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    msg_time: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    msg_seq: int = Field(None, jce_id=2)  # int16  `jceId:"2"`
    msg_cookies: Union[bytes, bytearray] = Field(None, jce_id=3)  # []byte `jceId:"3"`
    cmd: int = Field(None, jce_id=4)  # int16  `jceId:"4"`
    msg_type: int = Field(None, jce_id=5)  # int64  `jceId:"5"`
    app_id: int = Field(None, jce_id=6)  # int64  `jceId:"6"`
    send_time: int = Field(None, jce_id=7)  # int64  `jceId:"7"`
    sso_seq: int = Field(None, jce_id=8)  # int32  `jceId:"8"`
    sso_ip: int = Field(None, jce_id=9)  # int32  `jceId:"9"`
    client_ip: int = Field(None, jce_id=10)  # int32  `jceId:"10"`

    class Config:
        arbitrary_types_allowed = True


class FriendListRequest(BaseModel):
    req_type: int = Field(None, jce_id=0)  # int32   `jceId:"0"`
    if_reflush: Union[bytes, bytearray] = Field(None, jce_id=1)  # byte    `jceId:"1"`
    uin: int = Field(None, jce_id=2)  # int64   `jceId:"2"`
    start_index: int = Field(None, jce_id=3)  # int16   `jceId:"3"`
    friend_count: int = Field(None, jce_id=4)  # int16   `jceId:"4"`
    group_id: Union[bytes, bytearray] = Field(None, jce_id=5)  # byte    `jceId:"5"`
    if_get_group_info: Union[bytes, bytearray] = Field(None, jce_id=6)  # byte    `jceId:"6"`
    group_start_index: Union[bytes, bytearray] = Field(None, jce_id=7)  # byte    `jceId:"7"`
    group_count: Union[bytes, bytearray] = Field(None, jce_id=8)  # byte    `jceId:"8"`
    if_get_msf_group: Union[bytes, bytearray] = Field(None, jce_id=9)  # byte    `jceId:"9"`
    if_show_term_type: Union[bytes, bytearray] = Field(None, jce_id=10)  # byte    `jceId:"10"`
    version: int = Field(None, jce_id=11)  # int64   `jceId:"11"`
    uin_list: List[int] = Field(None, jce_id=12)  # []int64 `jceId:"12"`
    app_type: int = Field(None, jce_id=13)  # int32   `jceId:"13"`
    if_get_dovid: Union[bytes, bytearray] = Field(None, jce_id=14)  # byte    `jceId:"14"`
    if_get_both_flag: Union[bytes, bytearray] = Field(None, jce_id=15)  # byte    `jceId:"15"`
    d50: Union[bytes, bytearray] = Field(None, jce_id=16)  # []byte  `jceId:"16"`
    d6b: Union[bytes, bytearray] = Field(None, jce_id=17)  # []byte  `jceId:"17"`
    sns_type_list: List[int] = Field(None, jce_id=18)  # []int64 `jceId:"18"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class FriendInfo(IJceStruct):
    friend_uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    group_id: Union[bytes, bytearray] = Field(None, jce_id=1)  # byte   `jceId:"1"`
    face_id: int = Field(None, jce_id=2)  # int16  `jceId:"2"`
    remark: str = Field(None, jce_id=3)  # string `jceId:"3"`
    qq_type: Union[bytes, bytearray] = Field(None, jce_id=4)  # byte   `jceId:"4"`
    status: Union[bytes, bytearray] = Field(None, jce_id=5)  # byte   `jceId:"5"`
    member_level: Union[bytes, bytearray] = Field(None, jce_id=6)  # byte   `jceId:"6"`
    is_mqq_online: Union[bytes, bytearray] = Field(None, jce_id=7)  # byte   `jceId:"7"`
    qq_online_state: Union[bytes, bytearray] = Field(None, jce_id=8)  # byte   `jceId:"8"`
    is_iphone_online: Union[bytes, bytearray] = Field(None, jce_id=9)  # byte   `jceId:"9"`
    detail_status_flag: Union[bytes, bytearray] = Field(None, jce_id=10)  # byte   `jceId:"10"`
    qq_online_state_v2: Union[bytes, bytearray] = Field(None, jce_id=11)  # byte   `jceId:"11"`
    show_name: str = Field(None, jce_id=12)  # string `jceId:"12"`
    is_remark: Union[bytes, bytearray] = Field(None, jce_id=13)  # byte   `jceId:"13"`
    nick: str = Field(None, jce_id=14)  # string `jceId:"14"`
    special_flag: Union[bytes, bytearray] = Field(None, jce_id=15)  # byte   `jceId:"15"`
    im_group_id: Union[bytes, bytearray] = Field(None, jce_id=16)  # []byte `jceId:"16"`
    msf_group_id: Union[bytes, bytearray] = Field(None, jce_id=17)  # []byte `jceId:"17"`
    term_type: int = Field(None, jce_id=18)  # int32  `jceId:"18"`
    network: Union[bytes, bytearray] = Field(None, jce_id=20)  # byte   `jceId:"20"`
    ring: Union[bytes, bytearray] = Field(None, jce_id=21)  # []byte `jceId:"21"`
    abi_flag: int = Field(None, jce_id=22)  # int64  `jceId:"22"`
    face_addon_id: int = Field(None, jce_id=23)  # int64  `jceId:"23"`
    network_type: int = Field(None, jce_id=24)  # int32  `jceId:"24"`
    vip_font: int = Field(None, jce_id=25)  # int64  `jceId:"25"`
    icon_type: int = Field(None, jce_id=26)  # int32  `jceId:"26"`
    term_desc: str = Field(None, jce_id=27)  # string `jceId:"27"`
    color_ring: int = Field(None, jce_id=28)  # int64  `jceId:"28"`
    apollo_flag: Union[bytes, bytearray] = Field(None, jce_id=29)  # byte   `jceId:"29"`
    apollo_timestamp: int = Field(None, jce_id=30)  # int64  `jceId:"30"`
    sex: Union[bytes, bytearray] = Field(None, jce_id=31)  # byte   `jceId:"31"`
    founder_font: int = Field(None, jce_id=32)  # int64  `jceId:"32"`
    eim_id: str = Field(None, jce_id=33)  # string `jceId:"33"`
    eim_mobile: str = Field(None, jce_id=34)  # string `jceId:"34"`
    olympic_torch: Union[bytes, bytearray] = Field(None, jce_id=35)  # byte   `jceId:"35"`
    apollo_sign_time: int = Field(None, jce_id=36)  # int64  `jceId:"36"`
    lavi_uin: int = Field(None, jce_id=37)  # int64  `jceId:"37"`
    tag_update_time: int = Field(None, jce_id=38)  # int64  `jceId:"38"`
    game_last_login_time: int = Field(None, jce_id=39)  # int64  `jceId:"39"`
    game_app_id: int = Field(None, jce_id=40)  # int64  `jceId:"40"`
    card_id: Union[bytes, bytearray] = Field(None, jce_id=41)  # []byte `jceId:"41"`
    bitset: int = Field(None, jce_id=42)  # int64  `jceId:"42"`
    king_of_glory_flag: Union[bytes, bytearray] = Field(None, jce_id=43)  # byte   `jceId:"43"`
    king_of_glory_rank: int = Field(None, jce_id=44)  # int64  `jceId:"44"`
    master_uin: str = Field(None, jce_id=45)  # string `jceId:"45"`
    last_medal_update_time: int = Field(None, jce_id=46)  # int64  `jceId:"46"`
    face_store_id: int = Field(None, jce_id=47)  # int64  `jceId:"47"`
    font_effect: int = Field(None, jce_id=48)  # int64  `jceId:"48"`
    dov_id: str = Field(None, jce_id=49)  # string `jceId:"49"`
    both_flag: int = Field(None, jce_id=50)  # int64  `jceId:"50"`
    centi_show_3d_flag: Union[bytes, bytearray] = Field(None, jce_id=51)  # byte   `jceId:"51"`
    intimate_info: Union[bytes, bytearray] = Field(None, jce_id=52)  # []byte `jceId:"52"` 亲密度
    show_nameplate: Union[bytes, bytearray] = Field(None, jce_id=53)  # byte   `jceId:"53"`
    new_lover_diamond_flag: Union[bytes, bytearray] = Field(None, jce_id=54)  # byte   `jceId:"54"`
    ext_sns_frd_data: Union[bytes, bytearray] = Field(None, jce_id=55)  # []byte `jceId:"55"`
    mutual_mark_data: Union[bytes, bytearray] = Field(None, jce_id=56)  # []byte `jceId:"56"`

    def read_from(self, reader: JceReader):
        self.friend_uin = reader.read_int64(0)
        self.group_id = reader.read_byte(1)
        self.face_id = reader.read_int16(2)
        self.remark = reader.read_string(3)
        self.qq_type = reader.read_byte(4)
        self.status = reader.read_byte(5)
        self.member_level = reader.read_byte(6)
        self.is_mqq_online = reader.read_byte(7)
        self.qq_online_state = reader.read_byte(8)
        self.is_iphone_online = reader.read_byte(9)
        self.detail_status_flag = reader.read_byte(10)
        self.qq_online_state_v2 = reader.read_byte(11)
        self.show_name = reader.read_string(12)
        self.is_remark = reader.read_byte(13)
        self.nick = reader.read_string(14)
        self.special_flag = reader.read_byte(15)
        self.im_group_id = reader.read_any(16)
        self.msf_group_id = reader.read_any(17)
        self.term_type = reader.read_int32(18)
        self.network = reader.read_byte(20)
        self.ring = reader.read_any(21)
        self.abi_flag = reader.read_int64(22)
        self.face_addon_id = reader.read_int64(23)
        self.network_type = reader.read_int32(24)
        self.vip_font = reader.read_int64(25)
        self.icon_type = reader.read_int32(26)
        self.term_desc = reader.read_string(27)
        self.color_ring = reader.read_int64(28)
        self.apollo_flag = reader.read_byte(29)
        self.apollo_timestamp = reader.read_int64(30)
        self.sex = reader.read_byte(31)
        self.founder_font = reader.read_int64(32)
        self.eim_id = reader.read_string(33)
        self.eim_mobile = reader.read_string(34)
        self.olympic_torch = reader.read_byte(35)
        self.apollo_sign_time = reader.read_int64(36)
        self.lavi_uin = reader.read_int64(37)
        self.tag_update_time = reader.read_int64(38)
        self.game_last_login_time = reader.read_int64(39)
        self.game_app_id = reader.read_int64(40)
        self.card_id = reader.read_any(41)
        self.bitset = reader.read_int64(42)
        self.king_of_glory_flag = reader.read_byte(43)
        self.king_of_glory_rank = reader.read_int64(44)
        self.master_uin = reader.read_string(45)
        self.last_medal_update_time = reader.read_int64(46)
        self.face_store_id = reader.read_int64(47)
        self.font_effect = reader.read_int64(48)
        self.dov_id = reader.read_string(49)
        self.both_flag = reader.read_int64(50)
        self.centi_show_3d_flag = reader.read_byte(51)
        self.intimate_info = reader.read_any(52)
        self.show_nameplate = reader.read_byte(53)
        self.new_lover_diamond_flag = reader.read_byte(54)
        self.ext_sns_frd_data = reader.read_any(55)
        self.mutual_mark_data = reader.read_any(56)

    class Config:
        arbitrary_types_allowed = True


class TroopListRequest(IJceStruct):
    uin: int = Field(None, jce_id=0)  # int64   `jceId:"0"`
    get_msf_msg_flag: Union[bytes, bytearray] = Field(None, jce_id=1)  # byte    `jceId:"1"`
    cookies: Union[bytes, bytearray] = Field(None, jce_id=2)  # []byte  `jceId:"2"`
    group_info: List[int] = Field(None, jce_id=3)  # []int64 `jceId:"3"`
    group_flag_ext: Union[bytes, bytearray] = Field(None, jce_id=4)  # byte    `jceId:"4"`
    version: int = Field(None, jce_id=5)  # int32   `jceId:"5"`
    company_id: int = Field(None, jce_id=6)  # int64   `jceId:"6"`
    version_num: int = Field(None, jce_id=7)  # int64   `jceId:"7"`
    get_long_group_name: Union[bytes, bytearray] = Field(None, jce_id=8)  # byte    `jceId:"8"`

    def read_from(self, reader: JceReader):
        pass

    def to_bytes(self) -> bytes:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class TroopNumber(IJceStruct):
    group_uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    group_code: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    flag: Union[bytes, bytearray] = Field(None, jce_id=2)  # byte   `jceId:"2"`
    group_info_seq: int = Field(None, jce_id=3)  # int64  `jceId:"3"`
    group_name: str = Field(None, jce_id=4)  # string `jceId:"4"`
    group_memo: str = Field(None, jce_id=5)  # string `jceId:"5"`
    group_flag_ext: int = Field(None, jce_id=6)  # int64  `jceId:"6"`
    group_rank_seq: int = Field(None, jce_id=7)  # int64  `jceId:"7"`
    certification_type: int = Field(None, jce_id=8)  # int64  `jceId:"8"`
    shut_up_timestamp: int = Field(None, jce_id=9)  # int64  `jceId:"9"`
    my_shut_up_timestamp: int = Field(None, jce_id=10)  # int64  `jceId:"10"`
    cmd_uin_uin_flag: int = Field(None, jce_id=11)  # int64  `jceId:"11"`
    additional_flag: int = Field(None, jce_id=12)  # int64  `jceId:"12"`
    group_type_flag: int = Field(None, jce_id=13)  # int64  `jceId:"13"`
    group_sec_type: int = Field(None, jce_id=14)  # int64  `jceId:"14"`
    group_sec_type_info: int = Field(None, jce_id=15)  # int64  `jceId:"15"`
    group_class_ext: int = Field(None, jce_id=16)  # int64  `jceId:"16"`
    app_privilege_flag: int = Field(None, jce_id=17)  # int64  `jceId:"17"`
    subscription_uin: int = Field(None, jce_id=18)  # int64  `jceId:"18"`
    member_num: int = Field(None, jce_id=19)  # int64  `jceId:"19"`
    member_num_seq: int = Field(None, jce_id=20)  # int64  `jceId:"20"`
    member_card_seq: int = Field(None, jce_id=21)  # int64  `jceId:"21"`
    group_flag_ext3: int = Field(None, jce_id=22)  # int64  `jceId:"22"`
    group_owner_uin: int = Field(None, jce_id=23)  # int64  `jceId:"23"`
    is_conf_group: Union[bytes, bytearray] = Field(None, jce_id=24)  # byte   `jceId:"24"`
    is_modify_conf_group_face: Union[bytes, bytearray] = Field(None, jce_id=25)  # byte   `jceId:"25"`
    is_modify_conf_group_name: Union[bytes, bytearray] = Field(None, jce_id=26)  # byte   `jceId:"26"`
    cmd_uin_join_time: int = Field(None, jce_id=27)  # int64  `jceId:"27"`
    company_id: int = Field(None, jce_id=28)  # int64  `jceId:"28"`
    max_group_member_num: int = Field(None, jce_id=29)  # int64  `jceId:"29"`
    cmd_uin_group_mask: int = Field(None, jce_id=30)  # int64  `jceId:"30"`
    guild_app_id: int = Field(None, jce_id=31)  # int64  `jceId:"31"`
    guild_sub_type: int = Field(None, jce_id=32)  # int64  `jceId:"32"`
    cmd_uin_ringtone_id: int = Field(None, jce_id=33)  # int64  `jceId:"33"`
    cmd_uin_flag_ex2: int = Field(None, jce_id=34)  # int64  `jceId:"34"`

    def read_from(self, reader: JceReader):
        self.group_uin = reader.read_int64(0)
        self.group_code = reader.read_int64(1)
        self.flag = reader.read_byte(2)
        self.group_info_seq = reader.read_int64(3)
        self.group_name = reader.read_string(4)
        self.group_memo = reader.read_string(5)
        self.group_flag_ext = reader.read_int64(6)
        self.group_rank_seq = reader.read_int64(7)
        self.certification_type = reader.read_int64(8)
        self.shut_up_timestamp = reader.read_int64(9)
        self.my_shut_up_timestamp = reader.read_int64(10)
        self.cmd_uin_uin_flag = reader.read_int64(11)
        self.additional_flag = reader.read_int64(12)
        self.group_type_flag = reader.read_int64(13)
        self.group_sec_type = reader.read_int64(14)
        self.group_sec_type_info = reader.read_int64(15)
        self.group_class_ext = reader.read_int64(16)
        self.app_privilege_flag = reader.read_int64(17)
        self.subscription_uin = reader.read_int64(18)
        self.member_num = reader.read_int64(19)
        self.member_num_seq = reader.read_int64(20)
        self.member_card_seq = reader.read_int64(21)
        self.group_flag_ext3 = reader.read_int64(22)
        self.group_owner_uin = reader.read_int64(23)
        self.is_conf_group = reader.read_byte(24)
        self.is_modify_conf_group_face = reader.read_byte(25)
        self.is_modify_conf_group_name = reader.read_byte(26)
        self.cmd_uin_join_time = reader.read_int64(27)
        self.company_id = reader.read_int64(28)
        self.max_group_member_num = reader.read_int64(29)
        self.cmd_uin_group_mask = reader.read_int64(30)
        self.guild_app_id = reader.read_int64(31)
        self.guild_sub_type = reader.read_int64(32)
        self.cmd_uin_ringtone_id = reader.read_int64(33)
        self.cmd_uin_flag_ex2 = reader.read_int64(34)

    class Config:
        arbitrary_types_allowed = True


class TroopMemberListRequest(IJceStruct):
    uin: int = Field(None, jce_id=0)  # int64 `jceId:"0"`
    group_code: int = Field(None, jce_id=1)  # int64 `jceId:"1"`
    next_uin: int = Field(None, jce_id=2)  # int64 `jceId:"2"`
    group_uin: int = Field(None, jce_id=3)  # int64 `jceId:"3"`
    version: int = Field(None, jce_id=4)  # int64 `jceId:"4"`
    req_type: int = Field(None, jce_id=5)  # int64 `jceId:"5"`
    get_list_appoint_time: int = Field(None, jce_id=6)  # int64 `jceId:"6"`
    rich_card_name_ver: Union[bytes, bytearray] = Field(None, jce_id=7)  # byte  `jceId:"7"`

    def read_from(self, reader: JceReader):
        pass

    def to_bytes(self) -> bytes:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class TroopMemberInfo(BaseModel):
    member_uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    face_id: int = Field(None, jce_id=1)  # int16  `jceId:"1"`
    age: Union[bytes, bytearray] = Field(None, jce_id=2)  # byte   `jceId:"2"`
    gender: Union[bytes, bytearray] = Field(None, jce_id=3)  # byte   `jceId:"3"`
    nick: str = Field(None, jce_id=4)  # string `jceId:"4"`
    status: Union[bytes, bytearray] = Field(None, jce_id=5)  # byte   `jceId:"5"`
    show_name: str = Field(None, jce_id=6)  # string `jceId:"6"`
    name: str = Field(None, jce_id=8)  # string `jceId:"8"`
    memo: str = Field(None, jce_id=12)  # string `jceId:"12"`
    auto_remark: str = Field(None, jce_id=13)  # string `jceId:"13"`
    member_level: int = Field(None, jce_id=14)  # int64  `jceId:"14"`
    join_time: int = Field(None, jce_id=15)  # int64  `jceId:"15"`
    last_speak_time: int = Field(None, jce_id=16)  # int64  `jceId:"16"`
    credit_level: int = Field(None, jce_id=17)  # int64  `jceId:"17"`
    flag: int = Field(None, jce_id=18)  # int64  `jceId:"18"`
    flag_ext: int = Field(None, jce_id=19)  # int64  `jceId:"19"`
    point: int = Field(None, jce_id=20)  # int64  `jceId:"20"`
    concerned: Union[bytes, bytearray] = Field(None, jce_id=21)  # byte   `jceId:"21"`
    shielded: Union[bytes, bytearray] = Field(None, jce_id=22)  # byte   `jceId:"22"`
    special_title: str = Field(None, jce_id=23)  # string `jceId:"23"`
    special_titleexpire_time: int = Field(None, jce_id=24)  # int64  `jceId:"24"`
    job: str = Field(None, jce_id=25)  # string `jceId:"25"`
    apollo_flag: Union[bytes, bytearray] = Field(None, jce_id=26)  # byte   `jceId:"26"`
    apollo_timestamp: int = Field(None, jce_id=27)  # int64  `jceId:"27"`
    global_group_level: int = Field(None, jce_id=28)  # int64  `jceId:"28"`
    title_id: int = Field(None, jce_id=29)  # int64  `jceId:"29"`
    shutup_timestamp: int = Field(None, jce_id=30)  # int64  `jceId:"30"`
    global_group_point: int = Field(None, jce_id=31)  # int64  `jceId:"31"`
    rich_card_name_ver: Union[bytes, bytearray] = Field(None, jce_id=33)  # byte   `jceId:"33"`
    vip_type: int = Field(None, jce_id=34)  # int64  `jceId:"34"`
    vip_level: int = Field(None, jce_id=35)  # int64  `jceId:"35"`
    big_club_level: int = Field(None, jce_id=36)  # int64  `jceId:"36"`
    big_club_flag: int = Field(None, jce_id=37)  # int64  `jceId:"37"`
    nameplate: int = Field(None, jce_id=38)  # int64  `jceId:"38"`
    group_honor: Union[bytes, bytearray] = Field(None, jce_id=39)  # []byte `jceId:"39"`

    def read_from(self, reader: JceReader):
        self.member_uin = reader.read_int64(0)
        self.face_id = reader.read_int16(1)
        self.age = reader.read_byte(2)
        self.gender = reader.read_byte(3)
        self.nick = reader.read_string(4)
        self.status = reader.read_byte(5)
        self.show_name = reader.read_string(6)
        self.name = reader.read_string(8)
        self.memo = reader.read_string(12)
        self.auto_remark = reader.read_string(13)
        self.member_level = reader.read_int64(14)
        self.join_time = reader.read_int64(15)
        self.last_speak_time = reader.read_int64(16)
        self.credit_level = reader.read_int64(17)
        self.flag = reader.read_int64(18)
        self.flag_ext = reader.read_int64(19)
        self.point = reader.read_int64(20)
        self.concerned = reader.read_byte(21)
        self.shielded = reader.read_byte(22)
        self.special_title = reader.read_string(23)
        self.special_titleexpire_time = reader.read_int64(24)
        self.job = reader.read_string(25)
        self.apollo_flag = reader.read_byte(26)
        self.apollo_timestamp = reader.read_int64(27)
        self.global_group_level = reader.read_int64(28)
        self.title_id = reader.read_int64(29)
        self.shutup_timestamp = reader.read_int64(30)
        self.global_group_point = reader.read_int64(31)
        self.rich_card_name_ver = reader.read_byte(33)
        self.vip_type = reader.read_int64(34)
        self.vip_level = reader.read_int64(35)
        self.big_club_level = reader.read_int64(36)
        self.big_club_flag = reader.read_int64(37)
        self.nameplate = reader.read_int64(38)
        self.group_honor = reader.read_any(39)

    class Config:
        arbitrary_types_allowed = True


class ModifyGroupCardRequest(IJceStruct):
    zero: int = Field(None, jce_id=0)  # int64        `jceId:"0"`
    group_code: int = Field(None, jce_id=1)  # int64        `jceId:"1"`
    new_seq: int = Field(None, jce_id=2)  # int64        `jceId:"2"`
    uin_info: List[IJceStruct] = Field(None, jce_id=3)  # []IJceStruct `jceId:"3"`

    def read_from(self, reader: JceReader):
        pass

    def to_bytes(self) -> Union[bytes, bytearray]:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class UinInfo(IJceStruct):
    uin: int = Field(None, jce_id=0)  # int64  `jceId:"0"`
    flag: int = Field(None, jce_id=1)  # int64  `jceId:"1"`
    name: str = Field(None, jce_id=2)  # string `jceId:"2"`
    gender: Union[bytes, bytearray] = Field(None, jce_id=3)  # byte   `jceId:"3"`
    phone: str = Field(None, jce_id=4)  # string `jceId:"4"`
    email: str = Field(None, jce_id=5)  # string `jceId:"5"`
    remark: str = Field(None, jce_id=6)  # string `jceId:"6"`

    def read_from(self, reader: JceReader):
        pass

    class Config:
        arbitrary_types_allowed = True


class SummaryCardReq(IJceStruct):
    uin: int = Field(None, jce_id=0)  # int64 `jceId:"0"`
    come_from: int = Field(None, jce_id=1)  # int32 `jceId:"1"`
    qzone_feed_timestamp: int = Field(None, jce_id=2)  # int64 `jceId:"2"`
    is_friend: Union[bytes, bytearray] = Field(None, jce_id=3)  # byte  `jceId:"3"`
    group_code: int = Field(None, jce_id=4)  # int64 `jceId:"4"`
    group_uin: int = Field(None, jce_id=5)  # int64 `jceId:"5"`
    seed: Union[bytes, bytearray] = Field(None, jce_id=6)  # []byte`jceId:"6"`
    search_name: str = Field(None, jce_id=7)  # string`jceId:"7"`
    get_control: int = Field(None, jce_id=8)  # int64   `jceId:"8"`
    add_friend_source: int = Field(None, jce_id=9)  # int32   `jceId:"9"`
    secure_sig: Union[bytes, bytearray] = Field(None, jce_id=10)  # []byte  `jceId:"10"`
    tiny_id: int = Field(None, jce_id=15)  # int64   `jceId:"15"`
    like_source: int = Field(None, jce_id=16)  # int64   `jceId:"16"`
    req_medal_wall_info: Union[bytes, bytearray] = Field(None, jce_id=18)  # byte    `jceId:"18"`
    req_0x5eb_field_id: List[int] = Field(None, jce_id=19)  # []int64 `jceId:"19"`
    req_nearby_god_info: Union[bytes, bytearray] = Field(None, jce_id=20)  # byte    `jceId:"20"`
    req_extend_card: Union[bytes, bytearray] = Field(None, jce_id=22)  # byte    `jceId:"22"`

    def read_from(self, reader: JceReader):
        pass

    def to_bytes(self) -> Union[bytes, bytearray]:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True


class SummaryCardReqSearch(IJceStruct):
    keyword: str = Field(None, jce_id=0)  # string   `jceId:"0"`
    country_code: str = Field(None, jce_id=1)  # string   `jceId:"1"`
    version: int = Field(None, jce_id=2)  # int32    `jceId:"2"`
    req_services: List[bytes] = Field(None, jce_id=3)  # [][]byte `jceId:"3"` // busi

    def read_from(self, reader: JceReader):
        pass

    def to_bytes(self) -> Union[bytes, bytearray]:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    class Config:
        arbitrary_types_allowed = True
