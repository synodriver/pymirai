# -*- coding: utf-8 -*-
import unittest

from pyjce import JceReader

from pymirai.binary.jce.struct import RequestPacket
data = bytes.fromhex(
    "100129000b0a160e3139332e3131322e3233312e3630211f9030014c5c600870018602737a96066f74686572730b0a160d34322e38312e3137322e323135211f9030014c5c600870018602746a960374656c0b0a160b31342e32322e332e313134211f9030014c5c600870018602737a960374656c0b0a160e31342e3231352e3133382e3131302101bb30014c5c600870018602737a960374656c0b0a160d34322e38312e3136392e313030205030014c5c600870018602746a960374656c0b0a160e3131342e3232312e3134342e37362136b030014c5c6008700186027368960374656c0b0a160d3131332e39362e31322e3232342101bb30014c5c600870018602737a960374656c0b0a160d34322e38312e3137302e313232211f9030014c5c600870018602746a960374656c0b0a160e3131342e3232312e3134382e3637205030014c5c6008700186027368960374656c0b0a16116d7366776966692e33672e71712e636f6d211f9030014c5c60087c86066f746865727396066f74686572730b0a160c34322e38312e3137322e3633205030014c5c600870018602746a960374656c0b39000b0a160e3139332e3131322e3233312e3630211f9030014c5c600870018602737a96066f74686572730b0a160d34322e38312e3137322e323135211f9030014c5c600870018602746a960374656c0b0a160b31342e32322e332e313134211f9030014c5c600870018602737a960374656c0b0a160e31342e3231352e3133382e3131302101bb30014c5c600870018602737a960374656c0b0a160d34322e38312e3136392e313030205030014c5c600870018602746a960374656c0b0a160e3131342e3232312e3134342e37362136b030014c5c6008700186027368960374656c0b0a160d3131332e39362e31322e3232342101bb30014c5c600870018602737a960374656c0b0a160d34322e38312e3137302e313232211f9030014c5c600870018602746a960374656c0b0a160e3131342e3232312e3134382e3637205030014c5c6008700186027368960374656c0b0a16116d7366776966692e33672e71712e636f6d211f9030014c5c60087c86066f746865727396066f74686572730b0a160c34322e38312e3137322e3633205030014c5c600870018602746a960374656c0b425fe636545138406c7c80029005acbcc900050a160e3130392e3234342e3132392e3135205030014c500360087c8602737a96066f74686572730b0a160d34322e38312e3136392e313035205030014c500360087c8602746a960374656c0b0a160c3131332e39362e31332e3434205030014c500360087c8602737a960374656c0b0a160e3131342e3232312e3134342e3232205030014c500360087c86027368960374656c0b0a160d34322e38312e3136392e313035205030014c500360087c8602746a960374656c0bd900050a160e3130392e3234342e3132392e3135205030014c500360087c8602737a96066f74686572730b0a160d34322e38312e3136392e313035205030014c500360087c8602746a960374656c0b0a160c3131332e39362e31332e3434205030014c500360087c8602737a960374656c0b0a160e3131342e3232312e3134342e3232205030014c500360087c86027368960374656c0b0a160d34322e38312e3136392e313035205030014c500360087c8602746a960374656c0bed000cf90f0cf9100cf9110cf01202f113ff38f61428323032302d31322d32352032323a35383a32382064656c6976657279696e67206120706f6c6963790b")


class TestJce(unittest.TestCase):
    def test_decode(self):
        # with open("datas", "rb") as f:
        #     data = f.read()
        # reader = JceReader(b'\x1c,0\x01F\x0500000Pdb \x02\xf9\x0bv\x0f827817585121850\x8c\x9c\xac\xbc\xcc\xdc\xe0\x01')
        reader = JceReader(data)
        # while True:
        #     head, _ = reader.peak_head()
        #     print(reader.read_any(head.tag))
        SsoServerInfo_data = reader.read_list(2)
        print(SsoServerInfo_data)
        self.assertEqual(len(SsoServerInfo_data), 11)
        # self.assertEqual(reader.buffer.position,100)

    def test_jce_writer_schema(self):
        data = RequestPacket(iversion=1, cpacket_type=b"12", imessage_type=3, irequest_id=4, sservant_name="5",
                             sfunc_name="6", sbuffer=b"7", itimeout=8, context={"1": "2"}, status={"msg": "ok"})
        for field_name, val in data.schema()["properties"].items():
            jce_id: int = val["jce_id"]
            print(getattr(data, field_name), jce_id)


def main():
    pass


if __name__ == "__main__":
    main()
