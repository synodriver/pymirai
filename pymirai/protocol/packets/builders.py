# -*- coding: utf-8 -*-
import pymirai.binary as binary


def build_login_packet(uin: int,
                       body_type: int,
                       key: bytes,
                       body: bytes,
                       extra_data: bytes) -> bytes:
    """

    :param uin:
    :param body_type:
    :param key: tea key b""就是没有加密
    :param body:
    :param extra_data:
    :return:
    """
    w = binary.writer.Writer()

    def _lambda(w: binary.writer.Writer):
        w.write_uint32(0x0A)
        w.write_byte(body_type)

        def _lambda_2(w2: binary.writer.Writer):
            w2.write(extra_data)

        w.write_int_lv_packet(4, _lambda_2)
        w.write_byte(0x00)
        w.write_string(str(uin))
        if len(key) == 0:
            w.write(body)
        else:
            w.encrypt_and_write(key, body)

    w.write_int_lv_packet(4, _lambda)
    return bytes(w.bytes())


def build_uni_packet(uin: int, seq: int,
                     command_name: str,
                     encrypt_type: int,
                     session_id: bytes,
                     extra_data: bytes,
                     key: bytes,
                     body: bytes) -> bytes:
    def _lambda(w: binary.writer.Writer):
        w.write_uint32(0x0B)
        w.write_byte(encrypt_type)
        w.write_uint32(seq)
        w.write_byte(0)
        w.write_string(str(uin))

        w2 = binary.writer.Writer()
        w2.write_uni_packet(command_name, session_id, extra_data, body)

        w.encrypt_and_write(key, w2.bytes())

    w = binary.writer.Writer()
    w.write_int_lv_packet(4, _lambda)
    return bytes(w.bytes())
