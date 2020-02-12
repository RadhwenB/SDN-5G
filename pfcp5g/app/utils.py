import struct
from random import randint
import socket


def get_rand_seqNum():
    return toBytes(randint(0,16777215),3)

def sendPacket(packet,ip_address,port):
    sendsock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sendsock.settimeout(2)
    sendsock.sendto(packet,(ip_address,port))
    data, addr = sendsock.recvfrom(1024) # buffer size is 1024 bytes
    sendsock.close()
    return data
#Convert Int to Bytes STR, 2nd argument is the number of bytes of the output
def toBytes(value,bytesNumber):
    return struct.pack(">Q",value)[8-bytesNumber:]

def hexToInt(value):
    return int(value,16)

def parseIEs(IEs) :
    pass


def ipAddressToBytes(ipaddress) :
    IntStr=ipaddress.split('.')
    result=b''
    for i in IntStr :
        result=result+toBytes(int(i),1)
    return result

def createIEelement(Type,Value):
    return Type+struct.pack(">H", len(Value))+Value
