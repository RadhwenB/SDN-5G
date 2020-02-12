import struct


class PFCP:

    IEs=b''
    flags=b''
    messageType=b''
    length=b''
    seid=b''
    sequenceNumber=b''
    spare=b'\x00'

    def __init__(self,messageType,sequenceNumber,seid=None):

        if seid is None :
            self.flags=b'\x20'
        else :
            self.flags=b'\x21'
            self.seid=seid

        self.messageType=messageType
        self.sequenceNumber=sequenceNumber

    def getPacket(self) :
        declength=len(self.seid+self.sequenceNumber+self.spare+self.IEs)
        self.length=struct.pack(">H", declength)
        return(self.flags+self.messageType+self.length+self.seid+self.sequenceNumber+self.spare+self.IEs)

    def appendIE(self,Type,Value) :
        self.IEs+=Type+struct.pack(">H", len(Value))+Value
