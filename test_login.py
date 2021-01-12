from socket import socket, AF_INET, SOCK_STREAM
from pymirai.protocol.AndroidQQ import AndroidQQ


# # print(bytes2hex(int2bytes(2193096276,4)))
# Loginqq = AndroidQQ('uid', 'pwd', 0)
# # print(bytes2hex(Loginqq.Pack_Login()))
# s = socket(AF_INET, SOCK_STREAM)
# s.connect(("113.96.12.224", 8080))
# s.send(Loginqq.Pack_Login())
# buf = s.recv(2048)
# s.close()
# # print(bytes2hex(buf))
# Loginqq.Unpack_Login(buf)

# qq='2193096276'
# pack = Pack()
# pack.setShort(len(qq))
# pack.setStr(qq)
# pack.setHex('00 04')
# pack.setInt(int(qq))
# print(Str2Bytes('哈哈哈'))
# print(Bytes2Hex(pack.getAll()))

# a = Bytes2Hex(tea.encrypt(Str2Bytes('哈哈哈'),Hex2Bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
# print(a)
# b = Bytes2Hex(tea.decrypt(Hex2Bytes(a),Hex2Bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
# print(b)
class C:
    def __getattribute__(self, item):
        print("in __getattribute__")
        data = super().__getattribute__(item)
        return None

    def __getattr__(self, item):
        print("in ___getattr__")
        return None


C().a
