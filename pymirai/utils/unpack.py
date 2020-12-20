# -*- coding: utf-8 -*-

class Unpack(object):
    def __init__(self,pkt=bytes()):
        self.pkt = pkt
    
    def setData(self,pkt):
        self.pkt = pkt
    
    def getBin(self,num):
        ret = self.pkt[:num]
        self.pkt = self.pkt[num:]
        return ret

    def getInt(self):
        ret = self.pkt[:4]
        self.pkt = self.pkt[4:]
        ret = int.from_bytes(ret,byteorder='big')
        return ret
    
    def getShort(self):
        ret = self.pkt[:2]
        self.pkt = self.pkt[2:]
        ret = int.from_bytes(ret,byteorder='big')
        return ret
    
    def getAll(self):
        ret = self.pkt
        self.pkt = bytes()
        return ret