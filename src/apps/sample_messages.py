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
import src.utils.header_helper as ph
from src.proto.samples import mqtt_samples, coap_samples
from src.proto.protocol_codec import ProtocolDescription, ScapyCodec
from src.proto.protocol_description import ProtocolType
import src.utils.type_conversion as tc


def sample_messages(args):
    proto = args.proto

    if proto == 'mqtt':
        desc = ProtocolDescription(ProtocolType.MQTT)
        samples = mqtt_samples
    elif proto == 'coap':
        desc = ProtocolDescription(ProtocolType.CoAP)
        samples = coap_samples
    else:
        print('Protocol {} has no samples'.format(proto))
        sys.exit()

    codec = ScapyCodec(desc)

    # print a header
    header = ''*10 + 'Samples: {}'.format(desc.protocol_type) + ''*10
    ph.print_header(header)

    counter = 0
    for k, v in samples.items():
        counter += 1
        bytes_array = v.get('octstring')
        p = codec.decode_data(bytes_array)

        # print a separator with the counter
        print('{} [{} / {}] {}'.format('-'*30, counter, len(samples), '-'*30))

        print('Description: {}'.format(v.get('desc', 'No description given')))

        if 'note' in v:
            print('Note: {}'.format(v.get('note')))

        # Scapy's print function
        p.message.show2()

        if args.ls:
            print('### ls({}) ###'.format(p.message.summary()))
            codec.scapy.ls(p.message)
            print()  # empty line at the end

        if args.hex:
            print('### Hexdump({}) ###'.format(p.message.summary()))
            codec.scapy.hexdump(p.message)
            print()  # empty line at the end

        if args.bytes:
            print('### Python like bytearray ###')
            print(tc.bytearray2bytestring(bytes_array))
            print()  # empty line at the end

        if args.octets:
            print('### TTCN-3 like octetstring ###')
            print(tc.bytearray2octstring(bytes_array))
