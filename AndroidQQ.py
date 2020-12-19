from pymirai.utils.pack import Pack
from pymirai.utils.tlv import Tlv
from pymirai.utils.tea import Tea
from pymirai.utils.tools import *
import time
import hashlib

class AndroidQQ(object):
    def __init__(self,qq,password,xy):
        self.qq = qq
        self.password = password
        self.xy = xy #协议
        self.starttime = int(time.time())
        self.requestId = 10000
        self.tgtkey = getRandomBin(16)
        self.sharekey = hex2bytes('4A ED 5E CF F6 19 92 A8 BB 62 B3 A8 B3 C4 B0 8E')
        self.publickey = hex2bytes('04 5F FB B8 6D 00 A3 7F A9 9B 6A DB 6B C5 B1 75 B3 DD 51 5A FF 66 F6 04 76 85 BA 7F 66 69 69 D8 72 6F 4E 8F 40 B6 EC 17 80 F0 64 A5 51 2F 2B AD 18 5C C2 50 A9 4E BB 25 49 E4 D0 65 54 F9 66 0F A0')
        self.privatekey = hex2bytes('00 00 00 21 00 94 C7 25 8B 78 45 33 AB 23 73 B4 3A 60 AB 37 1D D4 53 3B 5A BD FB D6 43 C7 A2 3F CB 5A 08 01 A5')
        self.msgCookies = bytes()

        m = hashlib.md5()
        m.update(password.encode(encoding='utf-8'))
        self.md5pass = m.digest()
        m = hashlib.md5()
        m.update(self.md5pass + bytes(4) + int2bytes(int(self.qq),4))
        self.md52pass = m.digest()

        self.deviceguid = 'C3 6D 03 70 6B 7C 4E DD C0 77 46 91 C1 FB 91 F8'
        self.devicename = 'oppo r9 plustm a'
        self.devicebrand = 'oppo'
        self.deviceMac = '54 44 61 90 FC 9C 7E 08 C4 13 59 26 B8 73 4B C2'
        self.deviceImsi = '460001330114682'
        self.deviceimie = '865166024867445'
        self.ver = '|' + self.deviceImsi + '|A8.4.10.b8c39faf'
        self.bssid = ''
        self.ssid = 'dlb'
        self.AndroidId = 'CC 3C DD 51 8A 92 6C 6C 54 FF 46 48 CE E2 1D 29'
        self.appid = 537065990
        self.appid2 = 537065990
        self.main_signmap = 34869472
        self.apk_v = '8.4.10'
        self.apk_sig = 'A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D'
        self.apkid = 'com.tencent.mobileqq'
        self.sdkversion = '6.0.0.2438'

    def Pack_Login(self):
        pack = Pack()
        pack.write_short(9)
        pack.write_short(23) #23个tlv
        pack.write_bytes(Tlv.tlv018(self.qq))
        pack.write_bytes(Tlv.tlv001(self.qq,self.starttime))
        pack.write_bytes(Tlv.tlv106(self.qq,self.md5pass,self.md52pass,self.tgtkey,self.deviceguid,self.starttime,self.appid))
        pack.write_bytes(Tlv.tlv116(3))
        pack.write_bytes(Tlv.tlv100(self.appid,self.main_signmap))
        pack.write_bytes(Tlv.tlv107())
        pack.write_bytes(Tlv.tlv142(self.apkid))
        pack.write_bytes(Tlv.tlv144(self.tgtkey,Tlv.tlv109(self.AndroidId),Tlv.tlv124(),Tlv.tlv128(self.devicename,self.devicebrand,self.deviceguid),Tlv.tlv16E(self.devicename)))
        pack.write_bytes(Tlv.tlv145(self.deviceguid))
        pack.write_bytes(Tlv.tlv147(self.apk_v,self.apk_sig))
        pack.write_bytes(Tlv.tlv154(self.requestId))
        pack.write_bytes(Tlv.tlv141())
        pack.write_bytes(Tlv.tlv008())
        pack.write_bytes(Tlv.tlv511())
        pack.write_bytes(Tlv.tlv187(self.deviceMac))
        pack.write_bytes(Tlv.tlv188(self.deviceMac))
        pack.write_bytes(Tlv.tlv194(self.deviceImsi))
        pack.write_bytes(Tlv.tlv191())
        pack.write_bytes(Tlv.tlv202(self.bssid,self.ssid))
        pack.write_bytes(Tlv.tlv177(self.starttime,self.sdkversion))
        pack.write_bytes(Tlv.tlv516())
        pack.write_bytes(Tlv.tlv521())
        pack.write_bytes(Tlv.tlv525())

        pkt = Tea.encrypt(pack.get_all(),self.sharekey)
        pkt = self.Pack_LoginHead(pkt,0)
        pkt = self.Pack_Head(pkt,1)
        return pkt

    def Pack_LoginHead(self,pkt,mtype):
        pack = Pack()
        pack.write_int(self.requestId)
        pack.write_int(self.appid)
        pack.write_int(self.appid2)
        pack.write_hex('01 00 00 00 00 00 00 00 00 00 01 00 00 00 00 04')
        pack.write_int(17)
        pack.write_str('wtlogin.login')
        pack.write_hex('00 00 00 08')
        pack.write_bytes(getRandomBin(4))
        pack.write_int(len(self.deviceimie)+4)
        pack.write_str(self.deviceimie)
        if mtype == 2:
            pack.write_hex('00 00 00 14')
            pack.write_bytes(getRandomBin(16))
        else:
            pack.write_hex('00 00 00 04')
        pack.write_short(len(self.ver)+2)
        pack.write_str(self.ver)
        if self.xy == 1:
            pack.write_hex('00 00 00 04')
        else:
            pack.write_hex('00 00 00 2A')
            pack.write_hex('62 24 31 65 62 63 38 35 64 65 37 33 36 35 64 65 34 64 31 35 35 63 65 34 30 31 31 30 30 30 31 35 38 31 34 37 31 64')
        
        headpkt = pack.get_all()
        pack.set_empty()
        pack.write_int(len(headpkt)+4)
        pack.write_bytes(headpkt)
        headpkt = pack.get_all()

        pack.set_empty()
        pack.write_hex('1F 41 08 10 00 01')
        pack.write_int(int(self.qq))
        if self.xy == 1:
            pack.write_hex('03 87 00 00 00 00 02 00 00 00 00 00 00 00 00 01 01')
        elif mtype == 0:
            pack.write_hex('03 87 00 00 00 00 02 00 00 00 00 00 00 00 00 02 01')
        else:
            pack.write_hex('03 07 00 00 00 00 02 00 00 00 00 00 00 00 00 02 01')
        pack.write_bytes(getRandomBin(16))
        if self.xy == 1:
            pack.write_hex('01 02')
        elif mtype == 2:
            pack.write_hex('01 31 00 02')
        else:
            pack.write_hex('01 31 00 01')
        pack.write_short(len(self.publickey))
        pack.write_bytes(self.publickey)
        pack.write_bytes(pkt)

        pkt = pack.get_all()

        pack.set_empty()
        pack.write_hex('02')
        pack.write_short(len(pkt)+4)
        pack.write_bytes(pkt)
        pack.write_hex('03')

        pkt = pack.get_all()

        pack.set_empty()
        pack.write_bytes(headpkt)
        pack.write_int(len(pkt)+4)
        pack.write_bytes(pkt)

        pkt = Tea.encrypt(pack.get_all(),bytes(16))
        return pkt

    def Pack_Head(self,pkt,mtype):
        pack = Pack()
        if mtype == 1:
            pack.write_hex('00 00 00 0A 02 00 00 00 04')
        elif mtype == 2:
            pass
        elif mtype == 3:
            pack.write_hex('00 00 00 0B 01')
            pack.write_int(self.requestId)
        else:
            pack.write_hex('00 00 00 0B 02')
            pack.write_int(self.requestId)
        pack.write_hex('00 00 00')
        pack.write_short(len(self.qq)+4)
        pack.write_str(self.qq)
        pack.write_bytes(pkt)

        pkt = pack.get_all()

        pack.set_empty()
        pack.write_int(len(pkt)+4)
        pack.write_bytes(pkt)

        pkt = pack.get_all()
        return pkt
