
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
from app.TLV import TLV

PFCP_MSG = b'\x20'


#################################################
######### Sx Node Related Messages  #############
#################################################
TYPE_MSG_HEARTBEAT_REQUEST=b'\x01'
TYPE_MSG_HEARTBEAT_RESPONSE=b'\x02'
TYPE_MSG_PDF_MANAG_REQUEST=b'\x03'   # Sxb & Sxc only
TYPE_MSG_PDF_MANAG_RESPONSE=b'\x04'  # Sxb & Sxc only
TYPE_MSG_ASSOCIATION_SETUP_REQUEST=b'\x05'
TYPE_MSG_ASSOCIATION_SETUP_RESPONSE=b'\x06'
TYPE_MSG_ASSOCIATION_UPDATE_REQUEST=b'\x07'
TYPE_MSG_ASSOCIATION_UPDATE_RESPONSE=b'\x08'
TYPE_MSG_ASSOCIATION_RELEASE_REQUEST=b'\x09'
TYPE_MSG_ASSOCIATION_RELEASE_RESPONSE=b'\x0a'
TYPE_MSG_VERSION_NOT_SUPPORTED_RESPONSE=b'\x0b'
TYPE_MSG_NODE_REPORT_REQUEST=b'\x0c'
TYPE_MSG_NODE_REPORT_RESPONSE=b'\x0d'
TYPE_MSG_SESSION_SET_DELETION_REQUEST=b'\x0e'
TYPE_MSG_SESSION_SET_DELETION_RESPONSE=b'\x0f'



####################################################
######### Sx Session Related Messages  #############
####################################################
TYPE_MSG_SESSION_ESTABLISHEMENT_REQUEST=b'\x32'
TYPE_MSG_SESSION_ESTABLISHEMENT_RESPONSE=b'\x33'
TYPE_MSG_SESSION_MODIFICATION_REQUEST=b'\x34'
TYPE_MSG_SESSION_MODIFICATION_RESPONSE=b'\x35'
TYPE_MSG_SESSION_DELETION_REQUEST=b'\x36'
TYPE_MSG_SESSION_DELETION_RESPONSE=b'\x37'
TYPE_MSG_SESSION_REPORT_REQUEST=b'\x38'
TYPE_MSG_SESSION_REPORT_RESPONSE=b'\x39'


#################################
######### IE Types  #############
#################################
TYPE_IE_TIMESTAMP=b'\x00\x60'
TYPE_IE_NODE_ID=b'\x00\x3c'
TYPE_IE_UP_FUNCTION_FEATURES=b'\x00\x2b'
TYPE_IE_CP_FUNCTION_FEATURES=b'\x00\x59'
TYPE_IE_ASSOCIATION_RELEASE_REQUEST=b'\x00\x6f'
TYPE_IE_FSEID=b'\x00\x39'
TYPE_IE_CREATE_PDR=b'\x00\x01'
TYPE_IE_PACKET_DETECTION_RULE_ID=b'\x00\x38'
TYPE_IE_PRECEDENCE=b'\x00\x1d'
TYPE_IE_PDI=b'\x00\x02'
TYPE_IE_SOURCE_INTERFACE=b'\x00\x14'
TYPE_IE_DESTINATION_INTERFACE=b'\x00\x2a'
TYPE_IE_FTEID=b'\x00\x15'
TYPE_IE_UE_IP=b'\x00\x5d'
TYPE_IE_OUTER_HEADER_REMOVAL=b'\x00\x5F'
TYPE_IE_FAR_ID=b'\x00\x6c'
TYPE_IE_CREATE_FAR=b'\x00\x03'
TYPE_IE_APPLY_ACTION=b'\x00\x2c'
TYPE_IE_FORWARDING_PARAMETERS=b'\x00\x04'
TYPE_IE_SDF_FILTER=b'\x00\x17'

TYPE_NODE_ID_IPV4=b'\x00'

TYPE_CP_FEATURES_OVL=b'\x02'
TYPE_CP_FEATURES_LOAD=b'\x01'

#################################
##### Interfaces Types  #########
#################################
TYPE_INTERFACE_CORE=b'\x01'
TYPE_INTERFACE_ACCESS=b'\x00'

#################################
######## Actions Types  #########
#################################
TYPE_ACTION_DROP=b'\x01'
TYPE_ACTION_FORWARD=b'\x02'
TYPE_ACTION_BUFFER=b'\x04'
TYPE_ACTION_NOTIFY_CP=b'\x08'
TYPE_ACTION_DUPLICATE=b'\x10'


#################################
##### TLV Parser Dictionary #####
#################################
tlv = TLV(['0060','003c','002b','0013','0039','0008'])
