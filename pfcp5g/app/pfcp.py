
'''
Copyright 2020 ALIOUI Dhiaeddine, BOUAOUN Radhwen, PAPAGORA Niki from EURECOM

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
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
