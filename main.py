from _Pack import _Pack
from socket import socket,AF_INET,SOCK_STREAM
from Tools import *
from tea import tea

s=socket(AF_INET,SOCK_STREAM)
s.connect(("127.0.0.1",9999))
qq='2193096276'
pack = _Pack()
pack.setShort(len(qq))
pack.setStr(qq)
pack.setHex('00 04')
pack.setInt(int(qq))
s.send(pack.getAll())
s.close()

#print(Str2Bytes('哈哈哈'))
#print(Bytes2Hex(pack.getAll()))

a = Bytes2Hex(tea.encrypt(Str2Bytes('哈哈哈'),Hex2Bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
print(a)
b = Bytes2Hex(tea.decrypt(Hex2Bytes(a),Hex2Bytes('12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12')))
print(b)