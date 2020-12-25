# -*- coding: utf-8 -*-
import abc
from typing import Dict, List, Union

from pydantic import BaseModel, Field

from pymirai.binary.jce import JceReader, JceWriter


class IJceStruct(BaseModel, abc.ABC):
    @abc.abstractmethod
    def read_from(self, reader: JceReader):
        raise NotImplementedError


class RequestPacket(IJceStruct):  # todo 加入jceid标注
    iversion: int = Field(jce_id=1)  # int16   `jceId:"1"`
    cpacket_type: Union[bytes, bytearray] = Field(jce_id=2)  # byte              `jceId:"2"`
    imessage_type: int = Field(jce_id=3)  # int32             `jceId:"3"`
    irequest_id: int = Field(jce_id=4)  # int32             `jceId:"4"`
    sservant_name: str = Field(jce_id=5)  # string            `jceId:"5"`
    sfunc_name: str = Field(jce_id=6)  # string            `jceId:"6"`
    sbuffer: Union[bytes, bytearray] = Field(jce_id=7)  # []byte            `jceId:"7"`
    itimeout: int = Field(jce_id=8)  # int32             `jceId:"8"`
    context: Dict[str, str] = Field(jce_id=9)  # map[string]string `jceId:"9"`
    status: Dict[str, str] = Field(jce_id=10)  # map[string]string `jceId:"10"`

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
        self.sbuffer = reader.read_list(7)
        self.itimeout = reader.read_int32(8)
        self.context = reader.read_any(9)
        self.status = reader.read_any(10)


class RequestDataVersion3(IJceStruct):
    map: Dict[str, bytes] = Field(jce_id=0)  # map[string]map[string][]byte `jceId:"0"`

    def to_bytes(self) -> bytearray:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    def read_from(self, reader: JceReader):
        self.map = reader.read_any(0)


class RequestDataVersion2(IJceStruct):
    map: Dict[str, Dict[str, bytes]] = Field(jce_id=0)

    def to_bytes(self) -> bytearray:
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()

    def read_from(self, reader: JceReader):
        self.map = reader.read_any(0)


class SsoServerInfo(IJceStruct):
    server: str = Field(jce_id=1)  # string `jceId:"1"`
    port: int = Field(jce_id=2)  # int32  `jceId:"2"`
    location: str = Field(jce_id=3)  # string `jceId:"8"`

    def read_from(self, reader: JceReader):
        self.server = reader.read_string(1)
        self.port = reader.read_int32(2)
        self.location = reader.read_string(3)


class SvcReqRegister(BaseModel):
    uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    bid: int = Field(jce_id=1)  # int64  `jceId:"1"`
    conn_type: Union[bytes, bytearray] = Field(jce_id=2)  # byte   `jceId:"2"`
    other: str = Field(jce_id=3)  # string `jceId:"3"`
    status: int = Field(jce_id=4)  # int32  `jceId:"4"`
    online_push: Union[bytes, bytearray] = Field(jce_id=5)  # byte   `jceId:"5"`
    is_online: Union[bytes, bytearray] = Field(jce_id=6)  # byte   `jceId:"6"`
    is_show_online: Union[bytes, bytearray] = Field(jce_id=7)  # byte   `jceId:"7"`
    kick_pc: Union[bytes, bytearray] = Field(jce_id=8)  # byte   `jceId:"8"`
    kick_weak: Union[bytes, bytearray] = Field(jce_id=9)  # byte   `jceId:"9"`
    time_stamp: int = Field(jce_id=10)  # int64  `jceId:"10"`
    ios_version: int = Field(jce_id=11)  # int64  `jceId:"11"`
    net_type: Union[bytes, bytearray] = Field(jce_id=12)  # byte   `jceId:"12"`
    build_ver: str = Field(jce_id=13)  # string `jceId:"13"`
    reg_type: Union[bytes, bytearray] = Field(jce_id=14)  # byte   `jceId:"14"`
    dev_param: Union[bytes, bytearray] = Field(jce_id=15)  # []byte `jceId:"15"`
    guid: Union[bytes, bytearray] = Field(jce_id=16)  # []byte `jceId:"16"`
    locale_id: int = Field(jce_id=17)  # int32  `jceId:"17"`
    silent_push: Union[bytes, bytearray] = Field(jce_id=18)  # byte   `jceId:"18"`
    dev_name: str = Field(jce_id=19)  # string `jceId:"19"`
    dev_type: str = Field(jce_id=20)  # string `jceId:"20"`
    os_ver: str = Field(jce_id=21)  # string `jceId:"21"`
    open_push: Union[bytes, bytearray] = Field(jce_id=22)  # byte   `jceId:"22"`
    large_seq: int = Field(jce_id=23)  # int64  `jceId:"23"`
    last_watch_start_time: int = Field(jce_id=24)  # int64  `jceId:"24"`
    old_sso_ip: int = Field(jce_id=26)  # int64  `jceId:"26"`
    new_sso_ip: int = Field(jce_id=27)  # int64  `jceId:"27"`
    channel_no: str = Field(jce_id=28)  # string `jceId:"28"`
    cp_id: int = Field(jce_id=29)  # int64  `jceId:"29"`
    vendor_name: str = Field(jce_id=30)  # string `jceId:"30"`
    vendor_osname: str = Field(jce_id=31)  # string `jceId:"31"`
    ios_idfa: str = Field(jce_id=32)  # string `jceId:"32"`
    b769: Union[bytes, bytearray] = Field(jce_id=33)  # []byte `jceId:"33"`
    is_set_status: Union[bytes, bytearray] = Field(jce_id=34)  # byte   `jceId:"34"`
    server_buf: Union[bytes, bytearray] = Field(jce_id=35)  # []byte `jceId:"35"`
    set_mute: Union[bytes, bytearray] = Field(jce_id=36)  # byte   `jceId:"36"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()


class SvcRespRegister(IJceStruct):
    uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    bid: int = Field(jce_id=1)  # int64  `jceId:"1"`
    reply_code: Union[bytes, bytearray] = Field(jce_id=2)  # byte   `jceId:"2"`
    result: str = Field(jce_id=3)  # string `jceId:"3"`
    server_time: int = Field(jce_id=4)  # int64  `jceId:"4"`
    log_qq: Union[bytes, bytearray] = Field(jce_id=5)  # byte   `jceId:"5"`
    need_kik: Union[bytes, bytearray] = Field(jce_id=6)  # byte   `jceId:"6"`
    update_flag: Union[bytes, bytearray] = Field(jce_id=7)  # byte   `jceId:"7"`
    timestamp: int = Field(jce_id=8)  # int64  `jceId:"8"`
    crash_flag: Union[bytes, bytearray] = Field(jce_id=9)  # byte   `jceId:"9"`
    client_ip: str = Field(jce_id=10)  # string `jceId:"10"`
    client_port: int = Field(jce_id=11)  # int32  `jceId:"11"`
    hello_interval: int = Field(jce_id=12)  # int32  `jceId:"12"`
    large_seq: int = Field(jce_id=13)  # int32  `jceId:"13"`
    large_seq_update: Union[bytes, bytearray] = Field(jce_id=14)  # byte   `jceId:"14"`
    d769_rsp_body: Union[bytes, bytearray] = Field(jce_id=15)  # []byte `jceId:"15"`
    status: int = Field(jce_id=16)  # int32  `jceId:"16"`
    ext_online_status: int = Field(jce_id=17)  # int64  `jceId:"17"`
    client_battery_get_interval: int = Field(jce_id=18)  # int64  `jceId:"18"`
    client_auto_status_interval: int = Field(jce_id=19)  # int64  `jceId:"19"`

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


class PushMessageInfo(IJceStruct):  # 昵昵说不连续的jce是因为不需要那些 如广告
    from_uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    msg_time: int = Field(jce_id=1)  # int64  `jceId:"1"`
    msg_type: int = Field(jce_id=2)  # int16  `jceId:"2"`
    msg_seq: int = Field(jce_id=3)  # int16  `jceId:"3"`
    msg: str = Field(jce_id=4)  # string `jceId:"4"`
    real_msg_time: int = Field(jce_id=5)  # int32  `jceId:"5"`
    vmsg: Union[bytes, bytearray] = Field(jce_id=6)  # []byte `jceId:"6"`
    app_share_id: int = Field(jce_id=7)  # int64  `jceId:"7"`
    msg_cookies: Union[bytes, bytearray] = Field(jce_id=8)  # []byte `jceId:"8"`
    app_share_cookie: Union[bytes, bytearray] = Field(jce_id=9)  # []byte `jceId:"9"`
    msg_uid: int = Field(jce_id=10)  # int64  `jceId:"10"`
    last_change_time: int = Field(jce_id=11)  # int64  `jceId:"11"`
    from_inst_id: int = Field(jce_id=14)  # int64  `jceId:"14"`
    remark_of_sender: Union[bytes, bytearray] = Field(jce_id=15)  # []byte `jceId:"15"`
    from_mobile: str = Field(jce_id=16)  # string `jceId:"16"`
    from_name: str = Field(jce_id=17)  # string `jceId:"17"`

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


class SvcRespPushMsg(BaseModel):
    uin: int = Field(jce_id=0)  # int64        `jceId:"0"`
    del_infos: List[IJceStruct] = Field(jce_id=1)  # []IJceStruct `jceId:"1"`
    svr_ip: int = Field(jce_id=2)  # int32        `jceId:"2"`
    push_token: Union[bytes, bytearray] = Field(jce_id=3)  # []byte       `jceId:"3"`
    service_type: int = Field(jce_id=4)  # int32        `jceId:"4"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()


class SvcReqGetDevLoginInfo(BaseModel):
    guid: Union[bytes, bytearray] = Field(jce_id=0)  # []byte `jceId:"0"`
    app_name: str = Field(jce_id=1)  # string `jceId:"1"`
    login_type: int = Field(jce_id=2)  # int64  `jceId:"2"`
    time_stamp: int = Field(jce_id=3)  # int64  `jceId:"3"`
    next_item_index: int = Field(jce_id=4)  # int64  `jceId:"4"`
    require_max: int = Field(jce_id=5)  # int64  `jceId:"5"`
    get_dev_list_type: int = Field(
        jce_id=6)  # int64  1: getLoginDevList 2: getRecentLoginDevList 4: getAuthLoginDevList

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()


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


class DelMsgInfo(BaseModel):
    from_uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    msg_time: int = Field(jce_id=1)  # int64  `jceId:"1"`
    msg_seq: int = Field(jce_id=2)  # int16  `jceId:"2"`
    msg_cookies: Union[bytes, bytearray] = Field(jce_id=3)  # []byte `jceId:"3"`
    cmd: int = Field(jce_id=4)  # int16  `jceId:"4"`
    msg_type: int = Field(jce_id=5)  # int64  `jceId:"5"`
    app_id: int = Field(jce_id=6)  # int64  `jceId:"6"`
    send_time: int = Field(jce_id=7)  # int64  `jceId:"7"`
    sso_seq: int = Field(jce_id=8)  # int32  `jceId:"8"`
    sso_ip: int = Field(jce_id=9)  # int32  `jceId:"9"`
    client_ip: int = Field(jce_id=10)  # int32  `jceId:"10"`


class FriendListRequest(BaseModel):
    req_type: int = Field(jce_id=0)  # int32   `jceId:"0"`
    if_reflush: Union[bytes, bytearray] = Field(jce_id=1)  # byte    `jceId:"1"`
    uin: int = Field(jce_id=2)  # int64   `jceId:"2"`
    start_index: int = Field(jce_id=3)  # int16   `jceId:"3"`
    friend_count: int = Field(jce_id=4)  # int16   `jceId:"4"`
    group_id: Union[bytes, bytearray] = Field(jce_id=5)  # byte    `jceId:"5"`
    if_get_group_info: Union[bytes, bytearray] = Field(jce_id=6)  # byte    `jceId:"6"`
    group_start_index: Union[bytes, bytearray] = Field(jce_id=7)  # byte    `jceId:"7"`
    group_count: Union[bytes, bytearray] = Field(jce_id=8)  # byte    `jceId:"8"`
    if_get_msf_group: Union[bytes, bytearray] = Field(jce_id=9)  # byte    `jceId:"9"`
    if_show_term_type: Union[bytes, bytearray] = Field(jce_id=10)  # byte    `jceId:"10"`
    version: int = Field(jce_id=11)  # int64   `jceId:"11"`
    uin_list: List[int] = Field(jce_id=12)  # []int64 `jceId:"12"`
    app_type: int = Field(jce_id=13)  # int32   `jceId:"13"`
    if_get_dovid: Union[bytes, bytearray] = Field(jce_id=14)  # byte    `jceId:"14"`
    if_get_both_flag: Union[bytes, bytearray] = Field(jce_id=15)  # byte    `jceId:"15"`
    d50: Union[bytes, bytearray] = Field(jce_id=16)  # []byte  `jceId:"16"`
    d6b: Union[bytes, bytearray] = Field(jce_id=17)  # []byte  `jceId:"17"`
    sns_type_list: List[int] = Field(jce_id=18)  # []int64 `jceId:"18"`

    def to_bytes(self):
        writer = JceWriter()
        writer.write_jce_struct_raw(self)
        return writer.bytes()


class FriendInfo(IJceStruct):
    friend_uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    group_id: Union[bytes, bytearray] = Field(jce_id=1)  # byte   `jceId:"1"`
    face_id: int = Field(jce_id=2)  # int16  `jceId:"2"`
    remark: str = Field(jce_id=3)  # string `jceId:"3"`
    qq_type: Union[bytes, bytearray] = Field(jce_id=4)  # byte   `jceId:"4"`
    status: Union[bytes, bytearray] = Field(jce_id=5)  # byte   `jceId:"5"`
    member_level: Union[bytes, bytearray] = Field(jce_id=6)  # byte   `jceId:"6"`
    is_mqq_online: Union[bytes, bytearray] = Field(jce_id=7)  # byte   `jceId:"7"`
    qq_online_state: Union[bytes, bytearray] = Field(jce_id=8)  # byte   `jceId:"8"`
    is_iphone_online: Union[bytes, bytearray] = Field(jce_id=9)  # byte   `jceId:"9"`
    detail_status_flag: Union[bytes, bytearray] = Field(jce_id=10)  # byte   `jceId:"10"`
    qq_online_state_v2: Union[bytes, bytearray] = Field(jce_id=11)  # byte   `jceId:"11"`
    show_name: str = Field(jce_id=12)  # string `jceId:"12"`
    is_remark: Union[bytes, bytearray] = Field(jce_id=13)  # byte   `jceId:"13"`
    nick: str = Field(jce_id=14)  # string `jceId:"14"`
    special_flag: Union[bytes, bytearray] = Field(jce_id=15)  # byte   `jceId:"15"`
    im_group_id: Union[bytes, bytearray] = Field(jce_id=16)  # []byte `jceId:"16"`
    msf_group_id: Union[bytes, bytearray] = Field(jce_id=17)  # []byte `jceId:"17"`
    term_type: int = Field(jce_id=18)  # int32  `jceId:"18"`
    network: Union[bytes, bytearray] = Field(jce_id=20)  # byte   `jceId:"20"`
    ring: Union[bytes, bytearray] = Field(jce_id=21)  # []byte `jceId:"21"`
    abi_flag: int = Field(jce_id=22)  # int64  `jceId:"22"`
    face_addon_id: int = Field(jce_id=23)  # int64  `jceId:"23"`
    network_type: int = Field(jce_id=24)  # int32  `jceId:"24"`
    vip_font: int = Field(jce_id=25)  # int64  `jceId:"25"`
    icon_type: int = Field(jce_id=26)  # int32  `jceId:"26"`
    term_desc: str = Field(jce_id=27)  # string `jceId:"27"`
    color_ring: int = Field(jce_id=28)  # int64  `jceId:"28"`
    apollo_flag: Union[bytes, bytearray] = Field(jce_id=29)  # byte   `jceId:"29"`
    apollo_timestamp: int = Field(jce_id=30)  # int64  `jceId:"30"`
    sex: Union[bytes, bytearray] = Field(jce_id=31)  # byte   `jceId:"31"`
    founder_font: int = Field(jce_id=32)  # int64  `jceId:"32"`
    eim_id: str = Field(jce_id=33)  # string `jceId:"33"`
    eim_mobile: str = Field(jce_id=34)  # string `jceId:"34"`
    olympic_torch: Union[bytes, bytearray] = Field(jce_id=35)  # byte   `jceId:"35"`
    apollo_sign_time: int = Field(jce_id=36)  # int64  `jceId:"36"`
    lavi_uin: int = Field(jce_id=37)  # int64  `jceId:"37"`
    tag_update_time: int = Field(jce_id=38)  # int64  `jceId:"38"`
    game_last_login_time: int = Field(jce_id=39)  # int64  `jceId:"39"`
    game_app_id: int = Field(jce_id=40)  # int64  `jceId:"40"`
    card_id: Union[bytes, bytearray] = Field(jce_id=41)  # []byte `jceId:"41"`
    bitset: int = Field(jce_id=42)  # int64  `jceId:"42"`
    king_of_glory_flag: Union[bytes, bytearray] = Field(jce_id=43)  # byte   `jceId:"43"`
    king_of_glory_rank: int = Field(jce_id=44)  # int64  `jceId:"44"`
    master_uin: str = Field(jce_id=45)  # string `jceId:"45"`
    last_medal_update_time: int = Field(jce_id=46)  # int64  `jceId:"46"`
    face_store_id: int = Field(jce_id=47)  # int64  `jceId:"47"`
    font_effect: int = Field(jce_id=48)  # int64  `jceId:"48"`
    dov_id: str = Field(jce_id=49)  # string `jceId:"49"`
    both_flag: int = Field(jce_id=50)  # int64  `jceId:"50"`
    centi_show_3d_flag: Union[bytes, bytearray] = Field(jce_id=51)  # byte   `jceId:"51"`
    intimate_info: Union[bytes, bytearray] = Field(jce_id=52)  # []byte `jceId:"52"` 亲密度
    show_nameplate: Union[bytes, bytearray] = Field(jce_id=53)  # byte   `jceId:"53"`
    new_lover_diamond_flag: Union[bytes, bytearray] = Field(jce_id=54)  # byte   `jceId:"54"`
    ext_sns_frd_data: Union[bytes, bytearray] = Field(jce_id=55)  # []byte `jceId:"55"`
    mutual_mark_data: Union[bytes, bytearray] = Field(jce_id=56)  # []byte `jceId:"56"`

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
        # todo 写完这个


class TroopListRequest(IJceStruct):
    uin: int = Field(jce_id=0)  # int64   `jceId:"0"`
    get_msf_msg_flag: Union[bytes, bytearray] = Field(jce_id=1)  # byte    `jceId:"1"`
    cookies: Union[bytes, bytearray] = Field(jce_id=2)  # []byte  `jceId:"2"`
    group_info: List[int] = Field(jce_id=3)  # []int64 `jceId:"3"`
    group_flag_ext: Union[bytes, bytearray] = Field(jce_id=4)  # byte    `jceId:"4"`
    version: int = Field(jce_id=5)  # int32   `jceId:"5"`
    company_id: int = Field(jce_id=6)  # int64   `jceId:"6"`
    version_num: int = Field(jce_id=7)  # int64   `jceId:"7"`
    get_long_group_name: Union[bytes, bytearray] = Field(jce_id=8)  # byte    `jceId:"8"`

    def read_from(self, reader: JceReader):
        pass


class TroopNumber(BaseModel):
    group_uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    group_code: int = Field(jce_id=1)  # int64  `jceId:"1"`
    flag: Union[bytes, bytearray] = Field(jce_id=2)  # byte   `jceId:"2"`
    group_info_seq: int = Field(jce_id=3)  # int64  `jceId:"3"`
    group_name: str = Field(jce_id=4)  # string `jceId:"4"`
    group_memo: str = Field(jce_id=5)  # string `jceId:"5"`
    group_flag_ext: int = Field(jce_id=6)  # int64  `jceId:"6"`
    group_rank_seq: int = Field(jce_id=7)  # int64  `jceId:"7"`
    certification_type: int = Field(jce_id=8)  # int64  `jceId:"8"`
    shut_up_timestamp: int = Field(jce_id=9)  # int64  `jceId:"9"`
    my_shut_up_timestamp: int = Field(jce_id=10)  # int64  `jceId:"10"`
    cmd_uin_uin_flag: int = Field(jce_id=11)  # int64  `jceId:"11"`
    additional_flag: int = Field(jce_id=12)  # int64  `jceId:"12"`
    group_type_flag: int = Field(jce_id=13)  # int64  `jceId:"13"`
    group_sec_type: int = Field(jce_id=14)  # int64  `jceId:"14"`
    group_sec_type_info: int = Field(jce_id=15)  # int64  `jceId:"15"`
    group_class_ext: int = Field(jce_id=16)  # int64  `jceId:"16"`
    app_privilege_flag: int = Field(jce_id=17)  # int64  `jceId:"17"`
    subscription_uin: int = Field(jce_id=18)  # int64  `jceId:"18"`
    member_num: int = Field(jce_id=19)  # int64  `jceId:"19"`
    member_num_seq: int = Field(jce_id=20)  # int64  `jceId:"20"`
    member_card_seq: int = Field(jce_id=21)  # int64  `jceId:"21"`
    group_flag_ext3: int = Field(jce_id=22)  # int64  `jceId:"22"`
    group_owner_uin: int = Field(jce_id=23)  # int64  `jceId:"23"`
    is_conf_group: Union[bytes, bytearray] = Field(jce_id=24)  # byte   `jceId:"24"`
    is_modify_conf_group_face: Union[bytes, bytearray] = Field(jce_id=25)  # byte   `jceId:"25"`
    is_modify_conf_group_name: Union[bytes, bytearray] = Field(jce_id=26)  # byte   `jceId:"26"`
    cmd_uin_join_time: int = Field(jce_id=27)  # int64  `jceId:"27"`
    company_id: int = Field(jce_id=28)  # int64  `jceId:"28"`
    max_group_member_num: int = Field(jce_id=29)  # int64  `jceId:"29"`
    cmd_uin_group_mask: int = Field(jce_id=30)  # int64  `jceId:"30"`
    guild_app_id: int = Field(jce_id=31)  # int64  `jceId:"31"`
    guild_sub_type: int = Field(jce_id=32)  # int64  `jceId:"32"`
    cmd_uin_ringtone_id: int = Field(jce_id=33)  # int64  `jceId:"33"`
    cmd_uin_flag_ex2: int = Field(jce_id=34)  # int64  `jceId:"34"`


class TroopMemberListRequest(IJceStruct):
    uin: int = Field(jce_id=0)  # int64 `jceId:"0"`
    group_code: int = Field(jce_id=1)  # int64 `jceId:"1"`
    next_uin: int = Field(jce_id=2)  # int64 `jceId:"2"`
    group_uin: int = Field(jce_id=3)  # int64 `jceId:"3"`
    version: int = Field(jce_id=4)  # int64 `jceId:"4"`
    req_type: int = Field(jce_id=5)  # int64 `jceId:"5"`
    get_list_appoint_time: int = Field(jce_id=6)  # int64 `jceId:"6"`
    rich_card_name_ver: Union[bytes, bytearray] = Field(jce_id=7)  # byte  `jceId:"7"`

    def read_from(self, reader: JceReader):
        pass


class TroopMemberInfo(BaseModel):
    member_uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    face_id: int = Field(jce_id=1)  # int16  `jceId:"1"`
    age: Union[bytes, bytearray] = Field(jce_id=2)  # byte   `jceId:"2"`
    gender: Union[bytes, bytearray] = Field(jce_id=3)  # byte   `jceId:"3"`
    nick: str = Field(jce_id=4)  # string `jceId:"4"`
    status: Union[bytes, bytearray] = Field(jce_id=5)  # byte   `jceId:"5"`
    show_name: str = Field(jce_id=6)  # string `jceId:"6"`
    name: str = Field(jce_id=8)  # string `jceId:"8"`
    memo: str = Field(jce_id=12)  # string `jceId:"12"`
    auto_remark: str = Field(jce_id=13)  # string `jceId:"13"`
    member_level: int = Field(jce_id=14)  # int64  `jceId:"14"`
    join_time: int = Field(jce_id=15)  # int64  `jceId:"15"`
    last_speak_time: int = Field(jce_id=16)  # int64  `jceId:"16"`
    credit_level: int = Field(jce_id=17)  # int64  `jceId:"17"`
    flag: int = Field(jce_id=18)  # int64  `jceId:"18"`
    flag_ext: int = Field(jce_id=19)  # int64  `jceId:"19"`
    point: int = Field(jce_id=20)  # int64  `jceId:"20"`
    concerned: Union[bytes, bytearray] = Field(jce_id=21)  # byte   `jceId:"21"`
    shielded: Union[bytes, bytearray] = Field(jce_id=22)  # byte   `jceId:"22"`
    special_title: str = Field(jce_id=23)  # string `jceId:"23"`
    special_titleexpire_time: int = Field(jce_id=24)  # int64  `jceId:"24"`
    job: str = Field(jce_id=25)  # string `jceId:"25"`
    apollo_flag: Union[bytes, bytearray] = Field(jce_id=26)  # byte   `jceId:"26"`
    apollo_timestamp: int = Field(jce_id=27)  # int64  `jceId:"27"`
    global_group_level: int = Field(jce_id=28)  # int64  `jceId:"28"`
    title_id: int = Field(jce_id=29)  # int64  `jceId:"29"`
    shutup_timestamp: int = Field(jce_id=30)  # int64  `jceId:"30"`
    global_group_point: int = Field(jce_id=31)  # int64  `jceId:"31"`
    rich_card_name_ver: Union[bytes, bytearray] = Field(jce_id=33)  # byte   `jceId:"33"`
    vip_type: int = Field(jce_id=34)  # int64  `jceId:"34"`
    vip_level: int = Field(jce_id=35)  # int64  `jceId:"35"`
    big_club_level: int = Field(jce_id=36)  # int64  `jceId:"36"`
    big_club_flag: int = Field(jce_id=37)  # int64  `jceId:"37"`
    nameplate: int = Field(jce_id=38)  # int64  `jceId:"38"`
    group_honor: Union[bytes, bytearray] = Field(jce_id=39)  # []byte `jceId:"39"`


class ModifyGroupCardRequest(IJceStruct):
    zero: int = Field(jce_id=0)  # int64        `jceId:"0"`
    group_code: int = Field(jce_id=1)  # int64        `jceId:"1"`
    new_seq: int = Field(jce_id=2)  # int64        `jceId:"2"`
    uin_info: List[IJceStruct] = Field(jce_id=3)  # []IJceStruct `jceId:"3"`

    def read_from(self, reader: JceReader):
        pass


class UinInfo(IJceStruct):
    uin: int = Field(jce_id=0)  # int64  `jceId:"0"`
    flag: int = Field(jce_id=1)  # int64  `jceId:"1"`
    name: str = Field(jce_id=2)  # string `jceId:"2"`
    gender: Union[bytes, bytearray] = Field(jce_id=3)  # byte   `jceId:"3"`
    phone: str = Field(jce_id=4)  # string `jceId:"4"`
    email: str = Field(jce_id=5)  # string `jceId:"5"`
    remark: str = Field(jce_id=6)  # string `jceId:"6"`

    def read_from(self, reader: JceReader):
        pass


class SummaryCardReq(IJceStruct):
    uin: int = Field(jce_id=0)  # int64 `jceId:"0"`
    come_from: int = Field(jce_id=1)  # int32 `jceId:"1"`
    qzone_feed_timestamp: int = Field(jce_id=2)  # int64 `jceId:"2"`
    is_friend: Union[bytes, bytearray] = Field(jce_id=3)  # byte  `jceId:"3"`
    group_code: int = Field(jce_id=4)  # int64 `jceId:"4"`
    group_uin: int = Field(jce_id=5)  # int64 `jceId:"5"`
    seed: Union[bytes, bytearray] = Field(jce_id=6)  # []byte`jceId:"6"`
    search_name: str = Field(jce_id=7)  # string`jceId:"7"`
    get_control: int = Field(jce_id=8)  # int64   `jceId:"8"`
    add_friend_source: int = Field(jce_id=9)  # int32   `jceId:"9"`
    secure_sig: Union[bytes, bytearray] = Field(jce_id=10)  # []byte  `jceId:"10"`
    tiny_id: int = Field(jce_id=15)  # int64   `jceId:"15"`
    like_source: int = Field(jce_id=16)  # int64   `jceId:"16"`
    req_medal_wall_info: Union[bytes, bytearray] = Field(jce_id=18)  # byte    `jceId:"18"`
    req_0x5eb_field_id: List[int] = Field(jce_id=19)  # []int64 `jceId:"19"`
    req_nearby_god_info: Union[bytes, bytearray] = Field(jce_id=20)  # byte    `jceId:"20"`
    req_extend_card: Union[bytes, bytearray] = Field(jce_id=22)  # byte    `jceId:"22"`

    def read_from(self, reader: JceReader):
        pass


class SummaryCardReqSearch(IJceStruct):
    keyword: str = Field(jce_id=0)  # string   `jceId:"0"`
    country_code: str = Field(jce_id=1)  # string   `jceId:"1"`
    version: int = Field(jce_id=2)  # int32    `jceId:"2"`
    req_services: List[bytes] = Field(jce_id=3)  # [][]byte `jceId:"3"` // busi

    def read_from(self, reader: JceReader):
        pass
# todo 明天继续  先完成writer
