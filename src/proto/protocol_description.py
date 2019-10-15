# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************
from enum import Enum, auto
from src.proto.protocol_payload import PayloadType


class ProtocolType(Enum):
    """
    Enumerates the supported protocol modules
    """
    MQTT = auto(),
    CoAP = auto(),
    HTTP = auto(),
    UNKNOWN = auto()

    @staticmethod
    def supported_protocols(lower_case=True):
        """
        Gives a list of supported protocols. Mainly used for argparse to choose from
        :param lower_case:
        :return:
        """
        ret = ['MQTT', 'CoAP']
        if lower_case:
            return [e.lower() for e in ret]
        else:
            return ret

    def __str__(self):
        if self is ProtocolType.MQTT:
            return 'MQTT'
        elif self is ProtocolType.CoAP:
            return 'CoAP'
        elif self is ProtocolType.HTTP:
            return 'HTTP'
        else:
            return 'UNKNOWN PROTOCOL'

    @staticmethod
    def from_str(proto_type):
        proto_type = proto_type.upper()
        if proto_type == str(ProtocolType.MQTT):
            return ProtocolType.MQTT
        elif proto_type == str(ProtocolType.CoAP).upper():
            return ProtocolType.CoAP
        elif proto_type == str(ProtocolType.HTTP):
            return ProtocolType.HTTP
        else:
            return ProtocolType.UNKNOWN


class ProtocolMessageException(Exception):
    pass


# TODO: move ProtocolDescription to protocol_codec.py
class ProtocolDescription(object):

    def __init__(self, proto_type: ProtocolType, str_encoding='utf-8', payload_type: PayloadType = PayloadType.RAW):
        self._protocol_type = proto_type
        self._string_encoding = str_encoding
        self._payload_type = payload_type

    def __str__(self):
        return 'protocol={}, encoding={}, payload_field={}, payload_type={}' \
            .format(self.protocol_type, self.encoding, self.payload_field, self.payload_type)

    @property
    def protocol_type(self):
        return self._protocol_type

    @property
    def encoding(self):
        return self._string_encoding

    @property
    def payload_type(self):
        return self._payload_type

    @property
    def payload_field(self):
        """
        returns the field name of the payload field
        should result in: from <module.path> import <class>
        :return:
        """
        if self._protocol_type is ProtocolType.MQTT:
            return 'value'
        elif self._protocol_type is ProtocolType.CoAP:
            return 'TODO'   # TODO: how is the field called in Scapy?
        elif self._protocol_type is ProtocolType.HTTP:
            return 'TODO'   # TODO: how is the field called in Scapy?
        else:
            raise ProtocolMessageException('Protocol {} is not supported'.format(self))

    @property
    def ipl4_transport(self):
        # TODO: define Enum for supprted transport types
        """
        IP Layer 4 Transport Type
        :return:
        """
        if self._protocol_type is ProtocolType.MQTT:
            return 'tcp'
        elif self._protocol_type is ProtocolType.CoAP:
            return 'udp'
        elif self._protocol_type is ProtocolType.HTTP:
            return 'tcp'
        else:
            raise ProtocolMessageException('Protocol {} is not supported'.format(self))

    def get_module(self):
        """
        get's the path of the module and name class which can be used to dynamically import the right module and class
        should result in: from <module.path> import <class>
        :return:
        """
        if self._protocol_type is ProtocolType.MQTT:
            return 'scapy.contrib.mqtt', 'MQTT'
        elif self._protocol_type is ProtocolType.CoAP:
            return 'scapy.contrib.coap', 'CoAP'
        elif self._protocol_type is ProtocolType.HTTP:
            return 'scapy_http.http', 'HTTP'
        else:
            raise ProtocolMessageException('Protocol {} is not supported'.format(self))
