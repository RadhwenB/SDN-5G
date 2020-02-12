
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
import socket
from threading import Thread
import time
from app.TLV import TLV
from app.pfcp import PFCP
from app.pfcp_types import *
from app.routes import *
from app.__init__ import StartUpTimeStamp
from datetime import datetime


def receive():
    recv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    recv_sock.bind((Sx_ip_address, PFCP_PORT))
    while True:
        data, addr = recv_sock.recvfrom(1024) # buffer size is 1024 bytes
        #print( "Received PFCP packet :", data.hex())

        if(data[:1] == b'\x20') :
            if data[1:2] == b'\x05' :
                print("==== PFCP : Received ASSOCIATION REQUEST ====")
                association_request_handler(data,addr,recv_sock)
            elif data[1:2] == b'\x01':
                print("==== PFCP : Received HEARTBEAT REQUEST ====")
                heartbeat_request_handler(data,addr,recv_sock)
            else :
                pass
        else :
            pass

def association_request_handler(data,addr,sock) :

    currentAssociation = Association.query.filter_by(node_id=addr[0]).first()
    if currentAssociation == None :
        pass
    else :
        db.session.delete(currentAssociation)
        db.session.commit()

    pkt=PFCP(TYPE_MSG_ASSOCIATION_SETUP_RESPONSE,data[4:7])
    pkt.appendIE(TYPE_IE_NODE_ID,b'\x00'+ipAddressToBytes(Sx_ip_address))
    pkt.appendIE(TYPE_IE_TIMESTAMP,b'\xe1\x96\xb4\x92') # Time Stamp need to be coded
    pkt.appendIE(TYPE_IE_CP_FUNCTION_FEATURES,b'\x00')  # Supported Features of the CP missing
    sock.sendto(pkt.getPacket(),addr)
    newAssociation = Association(node_id = addr[0], creation_datetime=datetime.now())
    db.session.add(newAssociation)
    db.session.commit()
    t = Thread(target=liveness_thread_handler, args=(addr[0], ))
    t.start()



def send_heartbeat(addr):
    pkt=PFCP(TYPE_MSG_HEARTBEAT_REQUEST,get_rand_seqNum())
    pkt.appendIE(TYPE_IE_TIMESTAMP,StartUpTimeStamp)
    heartbeat_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        heartbeat_sock.settimeout(2)
        heartbeat_sock.sendto(pkt.getPacket(),(addr,PFCP_PORT))
        response, _ = heartbeat_sock.recvfrom(1024) # buffer size is 1024 bytes

    except socket.timeout:
        return False
    header = response.hex()[:16]
    IEs = response.hex()[16:]
    IEs=tlv.parse(IEs)
    heartbeat_sock.close()
    return True

def liveness_thread_handler(addr):

    def alive():
        counter = 0
        while (counter < 3):
            ok = send_heartbeat(addr)
            if not ok:
                counter = counter + 1
            else:
                counter = 0
            time.sleep(4)
        dead()

    def dead():
        while( True ) :
            ok = send_heartbeat(addr)
            if ok :
                rerequest_all_session(addr)
                alive()
            time.sleep(10)

    alive()


def rerequest_all_session(addr): # use the addr to retreive the sessions associated to this addr in the database
    print("Setting up all the related sessions ! ")
    pass

def heartbeat_request_handler(data,addr,sock) :
    pkt=PFCP(TYPE_MSG_HEARTBEAT_RESPONSE,data[4:7])
    pkt.appendIE(TYPE_IE_TIMESTAMP,StartUpTimeStamp)
    sock.sendto(pkt.getPacket(),addr)
