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

from abc import ABC, abstractmethod
import importlib

from src.proto.protocol_message import ProtocolDescription, AbstractMessage, ScapyMessage


class CodecException(Exception):
    pass


class AbstractCodec(ABC):

    def __init__(self, protocol: ProtocolDescription):
        self._protocol_descrption = protocol

    def __str__(self):
        return 'Codec({})'.format(self.protocol_description)

    @property
    def protocol_description(self):
        return self._protocol_descrption

    @abstractmethod
    def decode_data(self, data):
        pass

    @abstractmethod
    def encode_message(self, packet):
        pass


class ScapyCodec(AbstractCodec):

    def __init__(self, protocol: ProtocolDescription):
        super().__init__(protocol)

        # import the required scapy module
        self.scapy = importlib.import_module('scapy.all')
        module, constructor = protocol.get_module()
        scapy_proto_module = importlib.import_module(module)

        if not hasattr(scapy_proto_module, constructor):
            raise CodecException('{} cannot import {}.{}'.format(__class__, module, constructor))

        self.protocol_codec = getattr(scapy_proto_module, constructor)

    def decode_data(self, data):
        message = self.protocol_codec(data)
        scapy_message = ScapyMessage(self.protocol_description, message)

        return scapy_message

    def encode_message(self, message: AbstractMessage):
        message.payload_freeze()  # will encode the payload and set the encoded version in the raw message
        data = self.scapy.raw(message.message)
        return data

# TODO: what about additional protocol modules via Kaitai Struct or Construct?
# https://construct.readthedocs.io/en/latest/index.html
# https://kaitai.io/
# TODO: for that introduce a message class for a common interface to access message fields
