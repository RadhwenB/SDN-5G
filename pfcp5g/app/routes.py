
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
from flask import *
from flask import g
from app import app
from socket import *
import socket
import time
from app.TLV import TLV
from app.pfcp_types import *
from app.models import *
from app.pfcp import PFCP
from app.utils import *
from app.__init__ import StartUpTimeStamp
from datetime import datetime
from random import randint



Sx_ip_address="127.0.0.1"
PFCP_PORT = 8805


###########################################
########### Heartbeat Message #############
###########################################
#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x"
# }

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    user_data = request.json
    pkt=PFCP(TYPE_MSG_HEARTBEAT_REQUEST,get_rand_seqNum())
    pkt.appendIE(TYPE_IE_TIMESTAMP,StartUpTimeStamp)
    response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    header = response.hex()[:16]
    IEs = response.hex()[16:]
    IEs=tlv.parse(IEs)
    return ("Bootup Time : "+IEs['0060'])


###########################################
######### Association Procedures ##########
###########################################


#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x"
# }
@app.route('/association/setup', methods=['POST'])
def association_request():
    user_data = request.json
    pkt=PFCP(TYPE_MSG_ASSOCIATION_SETUP_REQUEST,toBytes(randint(0,16777215),3))
    dt = datetime.today()  # Get timezone naive no
    StartUpTimeStamp=toBytes(int (dt.strftime("%s")),4)
    pkt.appendIE(TYPE_IE_NODE_ID,TYPE_NODE_ID_IPV4+ipAddressToBytes(user_data['spgw_ip_address']))
    pkt.appendIE(TYPE_IE_TIMESTAMP,StartUpTimeStamp)
    pkt.appendIE(TYPE_IE_CP_FUNCTION_FEATURES,TYPE_CP_FEATURES_LOAD)

    response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    header = response.hex()[:16]
    IEs = response.hex()[16:]
    return str(tlv.parse(IEs))

###############################################
###### Association Release Procedures ########
###############################################

#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x"
# }
@app.route('/association/release', methods=['POST']) # The used OAI SPGW version does not support the Association Release
def association_release():
    user_data = request.json
    pkt=PFCP(TYPE_MSG_ASSOCIATION_RELEASE_REQUEST,toBytes(randint(0,16777215),3))

    pkt.appendIE(TYPE_IE_ASSOCIATION_RELEASE_REQUEST,b'\x00')
    try:
        response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    except socket.timeout:
        return "release failed ! Time out"
    association_deletion(userdata['spgw_ip_address'])
    return "successful release"

def association_deletion(spgw_ip_address):
    obj = Association.query.filter_by(node_id=spgw_ip_address).first()
    db.session.delete(obj)
    sessions = Session.query.filter_by(association_id = obj.id)
    db.session.delete(sessions)
    db.session.commit()


###########################################
########### Session Procedures ############
###########################################

#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x"
#   "in_interface":"access|core"
#   "ue_ip_address":"x.x.x.x"
#   "action":"forward|drop"
#   "out_interface":"access|core"
# }
@app.route('/session/request', methods=['POST'])
def session_request():
    user_data = request.json

    ##################### Verify JSON DATA #################################
    if user_data['in_interface'] == "core" :
        in_interface = TYPE_INTERFACE_CORE
    elif user_data['in_interface'] == "access" :
        in_interface = TYPE_INTERFACE_ACCESS
    else :
        return("in_interface ValueError, Value can be [access|core]")

    if user_data['action'] == "forward" :
        action = TYPE_ACTION_FORWARD
    elif user_data['action'] == "drop" :
        action = TYPE_ACTION_DROP
    else :
        return("action ValueError, Value can be [drop|forward]")

    if user_data['out_interface'] == "core" :
        out_interface = TYPE_INTERFACE_CORE
    elif user_data['out_interface'] == "access" :
        out_interface = TYPE_INTERFACE_ACCESS
    else :
        return("out_interface ValueError, Value can be [access|core]")
    ############################################################################

    seid=toBytes(0,8) #Seid = 0 because the Session dosen't yet exist,
    pkt=PFCP(TYPE_MSG_SESSION_ESTABLISHEMENT_REQUEST,get_rand_seqNum(),seid)
    pkt.appendIE(TYPE_IE_NODE_ID,TYPE_NODE_ID_IPV4+ipAddressToBytes(Sx_ip_address))

    cp_seid=toBytes(randint(0,100000000),8) #Choose a random and unique seid for the new established session

    FarID=toBytes(randint(0,65535),3) # Random FAR ID ( FAR is written on 31 bits,
                                    # but we will use only 3 bytes, other bits set to 0 )
                                    # left 1 byte ( 1 bit for allocation type and 7 bits for the FAR ID set to 0 )


    PdrID=toBytes(randint(0,65535),2) #Random PDR Rule ID

    pkt.appendIE(TYPE_IE_FSEID,b'\x02'+cp_seid+ipAddressToBytes(Sx_ip_address)) # \x02 pour IPv4
    pkt.appendIE(TYPE_IE_CREATE_PDR,
                createIEelement(TYPE_IE_PACKET_DETECTION_RULE_ID,PdrID) #Random PDR Rule ID
                +createIEelement(TYPE_IE_PRECEDENCE,b'\x00\x00\x00\x0f') # Precedence value = Priority Value of the RULE
                +createIEelement(TYPE_IE_PDI,
                             createIEelement(TYPE_IE_SOURCE_INTERFACE,in_interface)
                             +createIEelement(TYPE_IE_FTEID,b'\x04') # CHOOSE (CH) bit to 1 if the
                                                                    #UP function supports the allocation of F-TEID and the CP
                                                                    #function requests the UP function to assign a local FTEID to the PDR.
                             +createIEelement(TYPE_IE_UE_IP,b'\x02'+ipAddressToBytes(user_data['ue_ip_address'])) # \x02 pour IPv4
                             )
                +createIEelement(TYPE_IE_OUTER_HEADER_REMOVAL,b'\x00') # Do we have to select the GTU Header operation in the JSON or NOT !!
                +createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID) #Random FAR ID
                )

    if action == TYPE_ACTION_FORWARD : #Forward

        pkt.appendIE(TYPE_IE_CREATE_FAR,
                    createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID)  #\x00 : 1 bit = Allocation type, 7 bits = 7 MSB of FAR
                    +createIEelement(TYPE_IE_APPLY_ACTION,action)
                    +createIEelement(TYPE_IE_FORWARDING_PARAMETERS,
                                createIEelement(TYPE_IE_DESTINATION_INTERFACE,out_interface)
                             )
                    )
    else :  # Drop ( No need to add Forwarding Parameters )
        pkt.appendIE(TYPE_IE_CREATE_FAR,
                    createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID)
                    +createIEelement(TYPE_IE_APPLY_ACTION,action)
                    )


    response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    header = response.hex()[:32]
    IEs = response.hex()[32:]
    IEs = tlv.parse(IEs)
    if IEs['0013']=='01' :
        FSEID=IEs['0039']
        up_seid=FSEID[2:18]

        newSession = Session(cp_seid=int.from_bytes(cp_seid, "big") ,
                                up_seid=hexToInt(up_seid),
                                association_id=1,
                                source_interface=user_data['in_interface'],
                                destination_interface=user_data['out_interface'],
                                header_operation="",
                                action=user_data['action'],
                                ue_ip_address=user_data['ue_ip_address'],
                                creation_datetime=datetime.now())
        db.session.add(newSession)
        db.session.commit()
        db.session.close()

        return ("Session established with success : UP_SEID = "+ up_seid)
    else :
        return "Session request rejected !"

    return str(tlv.parse(IEs))



#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x",
#   "in_interface":"access|core",
#   "dest_ip_address":"x.x.x.x",
#   "dest_port":"x",
#   "action":"forward|drop",
#   "out_interface":"access|core"
# }

@app.route('/session/request/sdffilter', methods=['POST'])
def session_request_sdffilter():
    user_data = request.json

    ##################### Verify JSON DATA #################################
    if user_data['in_interface'] == "core" :
        in_interface = TYPE_INTERFACE_CORE
    elif user_data['in_interface'] == "access" :
        in_interface = TYPE_INTERFACE_ACCESS
    else :
        return("in_interface ValueError, Value can be [access|core]")

    if user_data['action'] == "forward" :
        action = TYPE_ACTION_FORWARD
    elif user_data['action'] == "drop" :
        action = TYPE_ACTION_DROP
    else :
        return("action ValueError, Value can be [drop|forward]")

    if user_data['out_interface'] == "core" :
        out_interface = TYPE_INTERFACE_CORE
    elif user_data['out_interface'] == "access" :
        out_interface = TYPE_INTERFACE_ACCESS
    else :
        return("out_interface ValueError, Value can be [access|core]")
    ############################################################################

    seid=toBytes(0,8) #Seid = 0 because the Session dosen't yet exist,
    pkt=PFCP(TYPE_MSG_SESSION_ESTABLISHEMENT_REQUEST,get_rand_seqNum(),seid)
    pkt.appendIE(TYPE_IE_NODE_ID,TYPE_NODE_ID_IPV4+ipAddressToBytes(Sx_ip_address))

    cp_seid=toBytes(randint(0,100000000),8) #Choose a random and unique seid for the new established session

    FarID=toBytes(randint(0,65535),3) # Random FAR ID ( FAR is written on 31 bits,
                                    # but we will use only 3 bytes, other bits set to 0 )
                                    # left 1 byte ( 1 bit for allocation type and 7 bits for the FAR ID set to 0 )


    PdrID=toBytes(randint(0,65535),2) #Random PDR Rule ID

    pkt.appendIE(TYPE_IE_FSEID,b'\x02'+cp_seid+ipAddressToBytes(Sx_ip_address)) # \x02 pour IPv4
    pkt.appendIE(TYPE_IE_CREATE_PDR,
                createIEelement(TYPE_IE_PACKET_DETECTION_RULE_ID,PdrID) #Random PDR Rule ID
                +createIEelement(TYPE_IE_PRECEDENCE,b'\x00\x00\x00\x0f') # Precedence value = Priority Value of the RULE
                +createIEelement(TYPE_IE_PDI,
                             createIEelement(TYPE_IE_SOURCE_INTERFACE,in_interface)
                             +createIEelement(TYPE_IE_SDF_FILTER,b'\x00\x00'+ipAddressToBytes("0.0.0.0") #Source IP address
                                                                            +toBytes(0,2)  # Source Port Number
                                                                            +ipAddressToBytes(user_data['dest_ip_address']) # Destination IP Address
                                                                            +toBytes(int(user_data['dest_port']),2)  # Destination Port Number
                                                                            +toBytes(0,1) # The protocol ID above IP
                                                                            ) # The SPGW needs to be programmed to understand this IE
                             )
                +createIEelement(TYPE_IE_OUTER_HEADER_REMOVAL,b'\x00') # Do we have to select the GTU Header operation in the JSON or NOT !!
                +createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID) #Random FAR ID
                )

    if action == TYPE_ACTION_FORWARD : #Forward

        pkt.appendIE(TYPE_IE_CREATE_FAR,
                    createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID)  #\x00 : 1 bit = Allocation type, 7 bits = 7 MSB of FAR
                    +createIEelement(TYPE_IE_APPLY_ACTION,action)
                    +createIEelement(TYPE_IE_FORWARDING_PARAMETERS,
                                createIEelement(TYPE_IE_DESTINATION_INTERFACE,out_interface)
                             )
                    )
    else :  # Drop ( No need to add Forwarding Parameters )
        pkt.appendIE(TYPE_IE_CREATE_FAR,
                    createIEelement(TYPE_IE_FAR_ID,b'\x00'+FarID)
                    +createIEelement(TYPE_IE_APPLY_ACTION,action)
                    )


    response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    header = response.hex()[:32]
    IEs = response.hex()[32:]
    IEs = tlv.parse(IEs)
    if IEs['0013']=='01' :
        FSEID=IEs['0039']
        up_seid=FSEID[2:18]

        newSession = Session(cp_seid=int.from_bytes(cp_seid, "big") ,
                                up_seid=hexToInt(up_seid),
                                association_id=1,
                                source_interface=user_data['in_interface'],
                                destination_interface=user_data['out_interface'],
                                header_operation="",
                                action=user_data['action'],
                                ue_ip_address=user_data['ue_ip_address'],
                                creation_datetime=datetime.now())
        db.session.add(newSession)
        db.session.commit()
        db.session.close()

        return ("Session established with success : UP_SEID = "+ up_seid)
    else :
        return "Session request rejected !"

    return str(tlv.parse(IEs))



###########################################
###### Session Deletion Procedures ########
###########################################

#### Expected JSON ###
# {
#   "spgw_ip_address":"x.x.x.x"
#   "seid":"x"
# }
@app.route('/session/deletion', methods=['POST'])
def session_deletion():
    user_data = request.json
    pkt=PFCP(TYPE_MSG_SESSION_DELETION_REQUEST,get_rand_seqNum(),toBytes(int(user_data['seid']),8))

    response=sendPacket(pkt.getPacket(),user_data['spgw_ip_address'],PFCP_PORT)
    header = response.hex()[:32]
    IEs = response.hex()[32:]
    IEs = tlv.parse(IEs)
    if IEs['0013']=='01' :
        sessions = Session.query.filter_by(up_seid = int(user_data['seid'])).first()
        db.session.delete(sessions)
        db.session.commit()
        return ("Session deleted with success : UP_SEID = "+ user_data['seid'])
    else :
        return "Session deletion request rejected !"

    return str(tlv.parse(IEs))






##############################################
########## Display Database Content ##########
##############################################
@app.route('/sessions/get', methods=['GET'])
def get_sessions():
    return str(Session.query.all())

@app.route('/associations/get', methods=['GET'])
def get_associations():
    return str(Association.query.all())



##########################################
############### Utils ####################
##########################################
@app.errorhandler(socket.timeout)
def handle_bad_request(e):
    return(str(e))



@app.route('/home', methods=['GET'])
def home():
    return("Hello !!")
