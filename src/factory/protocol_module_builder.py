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

from src.factory.abstract_builder import AbstractBuilder

from src.proto.protocol_codec import ScapyCodec
from src.proto.protocol_payload import PayloadType
from src.proto.protocol_description import ProtocolType, ProtocolDescription


class ProtocolModuleBuilder(AbstractBuilder):

    _protocol_name = None
    _string_encoding = None
    _payload = None

    @property
    def protocol_name(self):
        return self._protocol_name

    @protocol_name.setter
    def protocol_name(self, value):
        self._protocol_name = value

    @property
    def string_encoding(self):
        return self._string_encoding

    @string_encoding.setter
    def string_encoding(self, value):
        self._string_encoding = value

    def build_from_config(self, config):
        pm = config.get('protocolModule')

        payload = pm.get('payload', 'raw')
        payload_type = PayloadType.from_str(payload)

        protocol_type = ProtocolType.from_str(pm.get('protocol'))

        # HTTP can be already chosen from ProtocolType but not yet implemented!
        if protocol_type == ProtocolType.UNKNOWN or protocol_type == ProtocolType.HTTP:
            raise NotImplementedError('ProtocolModule for "{protocol}" not implemented'.format(**pm))

        str_encoding = pm.get('encoding', 'utf-8')

        protocol_description = ProtocolDescription(protocol_type, str_encoding, payload_type)

        return ScapyCodec(protocol_description)

    def build(self):
        raise NotImplementedError('stateful build of protocol module builder')
