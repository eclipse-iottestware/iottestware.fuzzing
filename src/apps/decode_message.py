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
import sys
import src.utils.type_conversion as tc
from src.proto.protocol_codec import ProtocolDescription, ScapyCodec
from src.proto.protocol_description import ProtocolType


def decode_message(args):
    input_value = args.input

    byte_array = ''   # empty init of output_value
    if args.o:
        byte_array = tc.octstring2bytearray(input_value)
    elif args.b:
        byte_array = tc.bytestring2bytearray(input_value)

    proto = args.proto

    if proto == 'mqtt':
        desc = ProtocolDescription(ProtocolType.MQTT)
    elif proto == 'coap':
        desc = ProtocolDescription(ProtocolType.CoAP)
    else:
        print('Protocol {} not supported'.format(proto))
        sys.exit()

    codec = ScapyCodec(desc)
    p = codec.decode_data(byte_array)

    if args.pdfdump:
        p.message.psdump()
    else:
        p.message.show2()
