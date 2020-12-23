# -*- coding: utf-8 -*-
import abc
from typing import Dict, List

from pydantic import BaseModel, Field

from pymirai.binary.jce import JceReader


class IJceStruct(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read_from(self, reader: JceReader):
        raise NotImplementedError


class RequestPacket(BaseModel):  # todo 加入jceid标注
    iversion: int = Field(jce_id=1)  # int16   `jceId:"1"`
    cpacket_type: bytes = Field(jce_id=2)  # byte              `jceId:"2"`
    imessage_type: int = Field(jce_id=3)  # int32             `jceId:"3"`
    irequest_id: int = Field(jce_id=4)  # int32             `jceId:"4"`
    sservant_name: str = Field(jce_id=5)  # string            `jceId:"5"`
    sfunc_name: str = Field(jce_id=6)  # string            `jceId:"6"`
    sbuffer: bytes = Field(jce_id=7)  # []byte            `jceId:"7"`
    itimeout: int = Field(jce_id=8)  # int32             `jceId:"8"`
    context: Dict[str, str] = Field(jce_id=9)  # map[string]string `jceId:"9"`
    status: Dict[str, str] = Field(jce_id=10)  # map[string]string `jceId:"10"`


class RequestDataVersion3(BaseModel):
    map: Dict[str, bytes]  # map[string]map[string][]byte `jceId:"0"`


class SsoServerInfo(BaseModel):
    server: str  # string `jceId:"1"`
    port: int  # int32  `jceId:"2"`
    location: str  # string `jceId:"8"`


class SvcReqRegister(BaseModel, IJceStruct):
    uin: int  # int64  `jceId:"0"`
    bid: int  # int64  `jceId:"1"`
    conn_type: bytes  # byte   `jceId:"2"`
    other: str  # string `jceId:"3"`
    status: int  # int32  `jceId:"4"`
    online_push: bytes  # byte   `jceId:"5"`
    is_online: bytes  # byte   `jceId:"6"`
    is_show_online: bytes  # byte   `jceId:"7"`
    kick_pc: bytes  # byte   `jceId:"8"`
    kick_weak: bytes  # byte   `jceId:"9"`
    time_stamp: int  # int64  `jceId:"10"`
    ios_version: int  # int64  `jceId:"11"`
    net_type: bytes  # byte   `jceId:"12"`
    build_ver: str  # string `jceId:"13"`
    reg_type: bytes  # byte   `jceId:"14"`
    dev_param: bytes  # []byte `jceId:"15"`
    guid: bytes  # []byte `jceId:"16"`
    locale_id: int  # int32  `jceId:"17"`
    silent_push: bytes  # byte   `jceId:"18"`
    dev_name: str  # string `jceId:"19"`
    dev_type: str  # string `jceId:"20"`
    os_ver: str  # string `jceId:"21"`
    open_push: bytes  # byte   `jceId:"22"`
    large_seq: int  # int64  `jceId:"23"`
    last_watch_start_time: int  # int64  `jceId:"24"`
    old_sso_ip: int  # int64  `jceId:"26"`
    new_sso_ip: int  # int64  `jceId:"27"`
    channel_no: str  # string `jceId:"28"`
    cp_id: int  # int64  `jceId:"29"`
    vendor_name: str  # string `jceId:"30"`
    vendor_osname: str  # string `jceId:"31"`
    ios_idfa: str  # string `jceId:"32"`
    b769: bytes  # []byte `jceId:"33"`
    is_set_status: bytes  # byte   `jceId:"34"`
    server_buf: bytes  # []byte `jceId:"35"`
    set_mute: bytes  # byte   `jceId:"36"`

    def read_from(self, reader: JceReader):
        pass


class SvcRespRegister(BaseModel):
    uin: int  # int64  `jceId:"0"`
    bid: int  # int64  `jceId:"1"`
    reply_code: bytes  # byte   `jceId:"2"`
    result: str  # string `jceId:"3"`
    server_time: int  # int64  `jceId:"4"`
    log_qq: bytes  # byte   `jceId:"5"`
    need_kik: bytes  # byte   `jceId:"6"`
    update_flag: bytes  # byte   `jceId:"7"`
    timestamp: int  # int64  `jceId:"8"`
    crash_flag: bytes  # byte   `jceId:"9"`
    client_ip: str  # string `jceId:"10"`
    client_port: int  # int32  `jceId:"11"`
    hello_interval: int  # int32  `jceId:"12"`
    large_seq: int  # int32  `jceId:"13"`
    large_seq_update: bytes  # byte   `jceId:"14"`
    d769_rsp_body: bytes  # []byte `jceId:"15"`
    status: int  # int32  `jceId:"16"`
    ext_online_status: int  # int64  `jceId:"17"`
    client_battery_get_interval: int  # int64  `jceId:"18"`
    client_auto_status_interval: int  # int64  `jceId:"19"`


class PushMessageInfo(BaseModel):
    from_uin: int  # int64  `jceId:"0"`
    msg_time: int  # int64  `jceId:"1"`
    msg_type: int  # int16  `jceId:"2"`
    msg_seq: int  # int16  `jceId:"3"`
    msg: str  # string `jceId:"4"`
    real_msg_time: int  # int32  `jceId:"5"`
    vmsg: bytes  # []byte `jceId:"6"`
    app_share_id: int  # int64  `jceId:"7"`
    msg_cookies: bytes  # []byte `jceId:"8"`
    app_share_cookie: bytes  # []byte `jceId:"9"`
    msg_uid: int  # int64  `jceId:"10"`
    last_change_Time: int  # int64  `jceId:"11"`
    from_inst_id: int  # int64  `jceId:"14"`
    remark_of_sender: bytes  # []byte `jceId:"15"`
    from_mobile: str  # string `jceId:"16"`
    from_name: str  # string `jceId:"17"`


class SvcRespPushMsg(BaseModel, IJceStruct):
    uin: int  # int64        `jceId:"0"`
    del_infos: List[IJceStruct]  # []IJceStruct `jceId:"1"`
    svr_ip: int  # int32        `jceId:"2"`
    push_token: bytes  # []byte       `jceId:"3"`
    service_type: int  # int32        `jceId:"4"`

    def read_from(self, reader: JceReader):
        pass


class SvcReqGetDevLoginInfo(BaseModel, IJceStruct):
    guid: bytes  # []byte `jceId:"0"`
    app_name: str  # string `jceId:"1"`
    login_type: int  # int64  `jceId:"2"`
    time_stamp: int  # int64  `jceId:"3"`
    next_item_index: int  # int64  `jceId:"4"`
    require_max: int  # int64  `jceId:"5"`
    get_dev_list_type: int  # int64  `jceId:"6"` // 1: getLoginDevList 2: getRecentLoginDevList 4: getAuthLoginDevList

    def read_from(self, reader: JceReader):
        pass


class SvcDevLoginInfo(BaseModel):
    app_id: int  # int64
    guid: bytes  # []byte
    login_time: int  # int64
    login_platform: int  # int64
    login_location: str  # string
    device_name: str  # string
    device_type_info: str  # string
    ter_type: int  # int64
    product_type: int  # int64
    can_be_kicked: int  # int64


class DelMsgInfo(BaseModel, IJceStruct):
    from_uin: int  # int64  `jceId:"0"`
    msg_time: int  # int64  `jceId:"1"`
    msg_seq: int  # int16  `jceId:"2"`
    msg_cookies: bytes  # []byte `jceId:"3"`
    cmd: int  # int16  `jceId:"4"`
    msg_type: int  # int64  `jceId:"5"`
    app_id: int  # int64  `jceId:"6"`
    send_time: int  # int64  `jceId:"7"`
    sso_seq: int  # int32  `jceId:"8"`
    sso_ip: int  # int32  `jceId:"9"`
    client_ip: int  # int32  `jceId:"10"`

    def read_from(self, reader: JceReader):
        pass


class FriendListRequest(BaseModel, IJceStruct):
    req_type: int  # int32   `jceId:"0"`
    if_reflush: bytes  # byte    `jceId:"1"`
    uin: int  # int64   `jceId:"2"`
    start_index: int  # int16   `jceId:"3"`
    friend_count: int  # int16   `jceId:"4"`
    group_id: bytes  # byte    `jceId:"5"`
    if_get_group_info: bytes  # byte    `jceId:"6"`
    group_start_index: bytes  # byte    `jceId:"7"`
    group_count: bytes  # byte    `jceId:"8"`
    if_get_msf_group: bytes  # byte    `jceId:"9"`
    if_show_term_type: bytes  # byte    `jceId:"10"`
    version: int  # int64   `jceId:"11"`
    uin_list: int  # []int64 `jceId:"12"`
    app_type: int  # int32   `jceId:"13"`
    if_get_dovid: bytes  # byte    `jceId:"14"`
    if_get_both_flag: bytes  # byte    `jceId:"15"`
    d50: bytes  # []byte  `jceId:"16"`
    d6b: bytes  # []byte  `jceId:"17"`
    sns_type_list: int  # []int64 `jceId:"18"`

    def read_from(self, reader: JceReader):
        pass


class FriendInfo(BaseModel):
    friend_uin: int  # int64  `jceId:"0"`
    group_id: int  # byte   `jceId:"1"`
    face_id: int  # int16  `jceId:"2"`
    remark: int  # string `jceId:"3"`
    qq_type: int  # byte   `jceId:"4"`
    status: int  # byte   `jceId:"5"`
    member_level: int  # byte   `jceId:"6"`
    is_mqq_online: int  # byte   `jceId:"7"`
    qq_online_state: int  # byte   `jceId:"8"`
    is_iphone_online: int  # byte   `jceId:"9"`
    detail_status_flag: int  # byte   `jceId:"10"`
    qq_online_state_v2: int  # byte   `jceId:"11"`
    show_name: int  # string `jceId:"12"`
    is_remark: int  # byte   `jceId:"13"`
    nick: int  # string `jceId:"14"`
    special_flag: int  # byte   `jceId:"15"`
    im_group_id: int  # []byte `jceId:"16"`
    msf_group_id: int  # []byte `jceId:"17"`
    term_type: int  # int32  `jceId:"18"`
    network: int  # byte   `jceId:"20"`
    ring: int  # []byte `jceId:"21"`
    abi_flag: int  # int64  `jceId:"22"`
    face_addon_id: int  # int64  `jceId:"23"`
    network_type: int  # int32  `jceId:"24"`
    vip_font: int  # int64  `jceId:"25"`
    icon_type: int  # int32  `jceId:"26"`
    term_desc: int  # string `jceId:"27"`
    color_ring: int  # int64  `jceId:"28"`
    apollo_flag: int  # byte   `jceId:"29"`
    apollo_timestamp: int  # int64  `jceId:"30"`
    sex: int  # byte   `jceId:"31"`
    founder_font: int  # int64  `jceId:"32"`
    eim_id: int  # string `jceId:"33"`
    eim_mobile: int  # string `jceId:"34"`
    olympic_torch: int  # byte   `jceId:"35"`
    apollo_sign_time: int  # int64  `jceId:"36"`
    lavi_uin: int  # int64  `jceId:"37"`
    tag_update_time: int  # int64  `jceId:"38"`
    game_last_login_time: int  # int64  `jceId:"39"`
    game_app_id: int  # int64  `jceId:"40"`
    card_id: int  # []byte `jceId:"41"`
    bitset: int  # int64  `jceId:"42"`
    king_of_glory_flag: int  # byte   `jceId:"43"`
    king_of_glory_rank: int  # int64  `jceId:"44"`
    master_uin: int  # string `jceId:"45"`
    last_medal_update_time: int  # int64  `jceId:"46"`
    face_store_id: int  # int64  `jceId:"47"`
    font_effect: int  # int64  `jceId:"48"`
    dov_id: int  # string `jceId:"49"`
    both_flag: int  # int64  `jceId:"50"`
    centi_show_3d_flag: int  # byte   `jceId:"51"`
    intimate_info: int  # []byte `jceId:"52"` 亲密度
    show_nameplate: int  # byte   `jceId:"53"`
    new_lover_diamond_flag: int  # byte   `jceId:"54"`
    ext_sns_frd_data: int  # []byte `jceId:"55"`
    mutual_mark_data: int  # []byte `jceId:"56"`


class TroopListRequest(BaseModel, IJceStruct):
    uin: int  # int64   `jceId:"0"`
    get_msf_msg_flag: bytes  # byte    `jceId:"1"`
    cookies: bytes  # []byte  `jceId:"2"`
    group_info: int  # []int64 `jceId:"3"`
    group_flag_ext: bytes  # byte    `jceId:"4"`
    version: int  # int32   `jceId:"5"`
    company_id: int  # int64   `jceId:"6"`
    version_num: int  # int64   `jceId:"7"`
    get_long_group_name: bytes  # byte    `jceId:"8"`

    def read_from(self, reader: JceReader):
        pass


class TroopNumber(BaseModel):
    group_uin: int  # int64  `jceId:"0"`
    group_code: int  # int64  `jceId:"1"`
    flag: bytes  # byte   `jceId:"2"`
    group_info_seq: int  # int64  `jceId:"3"`
    group_name: int  # string `jceId:"4"`
    group_memo: int  # string `jceId:"5"`
    group_flag_ext: int  # int64  `jceId:"6"`
    group_rank_seq: int  # int64  `jceId:"7"`
    certification_type: int  # int64  `jceId:"8"`
    shut_up_timestamp: int  # int64  `jceId:"9"`
    my_shut_up_timestamp: int  # int64  `jceId:"10"`
    cmd_uin_uin_flag: int  # int64  `jceId:"11"`
    additional_flag: int  # int64  `jceId:"12"`
    group_type_flag: int  # int64  `jceId:"13"`
    group_sec_type: int  # int64  `jceId:"14"`
    group_sec_type_info: int  # int64  `jceId:"15"`
    group_class_ext: int  # int64  `jceId:"16"`
    app_privilege_flag: int  # int64  `jceId:"17"`
    subscription_uin: int  # int64  `jceId:"18"`
    member_num: int  # int64  `jceId:"19"`
    member_num_seq: int  # int64  `jceId:"20"`
    member_card_seq: int  # int64  `jceId:"21"`
    group_flag_ext3: int  # int64  `jceId:"22"`
    group_owner_uin: int  # int64  `jceId:"23"`
    is_conf_group: int  # byte   `jceId:"24"`
    is_modify_conf_group_face: int  # byte   `jceId:"25"`
    is_modify_conf_group_name: int  # byte   `jceId:"26"`
    cmd_uin_join_time: int  # int64  `jceId:"27"`
    company_id: int  # int64  `jceId:"28"`
    max_group_member_num: int  # int64  `jceId:"29"`
    cmd_uin_group_mask: int  # int64  `jceId:"30"`
    guild_app_id: int  # int64  `jceId:"31"`
    guild_sub_type: int  # int64  `jceId:"32"`
    cmd_uin_ringtone_id: int  # int64  `jceId:"33"`
    cmd_uin_flag_ex2: int  # int64  `jceId:"34"`


class TroopMemberListRequest(BaseModel, IJceStruct):
    uin: int  # int64 `jceId:"0"`
    group_code: int  # int64 `jceId:"1"`
    next_uin: int  # int64 `jceId:"2"`
    group_uin: int  # int64 `jceId:"3"`
    version: int  # int64 `jceId:"4"`
    req_type: int  # int64 `jceId:"5"`
    get_list_appoint_time: int  # int64 `jceId:"6"`
    rich_card_name_ver: bytes  # byte  `jceId:"7"`

    def read_from(self, reader: JceReader):
        pass


class TroopMemberInfo(BaseModel):
    member_uin: int  # int64  `jceId:"0"`
    face_id: int  # int16  `jceId:"1"`
    age: bytes  # byte   `jceId:"2"`
    gender: bytes  # byte   `jceId:"3"`
    nick: str  # string `jceId:"4"`
    status: bytes  # byte   `jceId:"5"`
    show_name: str  # string `jceId:"6"`
    name: str  # string `jceId:"8"`
    memo: str  # string `jceId:"12"`
    auto_remark: str  # string `jceId:"13"`
    member_level: int  # int64  `jceId:"14"`
    join_time: int  # int64  `jceId:"15"`
    last_speak_time: int  # int64  `jceId:"16"`
    credit_level: int  # int64  `jceId:"17"`
    flag: int  # int64  `jceId:"18"`
    flag_ext: int  # int64  `jceId:"19"`
    point: int  # int64  `jceId:"20"`
    concerned: bytes  # byte   `jceId:"21"`
    shielded: bytes  # byte   `jceId:"22"`
    special_title: str  # string `jceId:"23"`
    special_titleexpire_time: int  # int64  `jceId:"24"`
    job: str  # string `jceId:"25"`
    apollo_flag: bytes  # byte   `jceId:"26"`
    apollo_timestamp: int  # int64  `jceId:"27"`
    global_group_level: int  # int64  `jceId:"28"`
    title_id: int  # int64  `jceId:"29"`
    shutup_timestamp: int  # int64  `jceId:"30"`
    global_group_point: int  # int64  `jceId:"31"`
    rich_card_name_ver: bytes  # byte   `jceId:"33"`
    vip_type: int  # int64  `jceId:"34"`
    vip_level: int  # int64  `jceId:"35"`
    big_club_level: int  # int64  `jceId:"36"`
    big_club_flag: int  # int64  `jceId:"37"`
    nameplate: int  # int64  `jceId:"38"`
    group_honor: bytes  # []byte `jceId:"39"`


class ModifyGroupCardRequest(BaseModel, IJceStruct):
    zero: int  # int64        `jceId:"0"`
    group_code: int  # int64        `jceId:"1"`
    new_seq: int  # int64        `jceId:"2"`
    uin_info: List[IJceStruct]  # []IJceStruct `jceId:"3"`

    def read_from(self, reader: JceReader):
        pass


class UinInfo(BaseModel, IJceStruct):
    uin: int  # int64  `jceId:"0"`
    flag: int  # int64  `jceId:"1"`
    name: str  # string `jceId:"2"`
    gender: bytes  # byte   `jceId:"3"`
    phone: str  # string `jceId:"4"`
    email: str  # string `jceId:"5"`
    remark: str  # string `jceId:"6"`

    def read_from(self, reader: JceReader):
        pass


class SummaryCardReq(BaseModel, IJceStruct):
    uin: int  # int64 `jceId:"0"`
    come_from: int  # int32 `jceId:"1"`
    qzone_feed_timestamp: int  # int64 `jceId:"2"`
    is_friend: bytes  # byte  `jceId:"3"`
    group_code: int  # int64 `jceId:"4"`
    group_uin: int  # int64 `jceId:"5"`
    seed: bytes  # []byte`jceId:"6"`
    search_name: str  # string`jceId:"7"`
    get_control: int  # int64   `jceId:"8"`
    add_friend_source: int  # int32   `jceId:"9"`
    secure_sig: bytes  # []byte  `jceId:"10"`
    tiny_id: int  # int64   `jceId:"15"`
    like_source: int  # int64   `jceId:"16"`
    req_medal_wall_info: bytes  # byte    `jceId:"18"`
    req_0x5eb_field_id: List[int]  # []int64 `jceId:"19"`
    req_nearby_god_info: bytes  # byte    `jceId:"20"`
    req_extend_card: bytes  # byte    `jceId:"22"`

    def read_from(self, reader: JceReader):
        pass


class SummaryCardReqSearch(BaseModel, IJceStruct):
    keyword: str  # string   `jceId:"0"`
    country_code: str  # string   `jceId:"1"`
    version: int  # int32    `jceId:"2"`
    req_services: List[bytes]  # [][]byte `jceId:"3"` // busi

    def read_from(self, reader: JceReader):
        pass
# todo 明天继续  先完成writer
