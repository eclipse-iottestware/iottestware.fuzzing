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
import src.utils.type_conversion as tc
# this is a collection of example messages for the supported protocols
# these can be used either for testing purposes and for checking scapy's field names

# TODO: move somewhere else from here! (probably to tests or own package?)

mqtt_samples = {
    'connect_01': {
        'desc': 'Connect message from TC_MQTT_BROKER_CONNECT_001',
        'octstring': tc.octstring2bytearray('1F1300044D515454040200140007434C49454E5431')
    },
    'connect_02': {
        'desc': 'Connect with LWT',
        'octstring': tc.octstring2bytearray('109E0100044D51545404EE00140007434C49454E5431003D65636C697073652F696F742'
                                            'F74657374776172652F34626234313563382D326335622D343861662D396130652D3436'
                                            '633334663736373266372F4C5754000C57696C6C204D657373616765002432363037643'
                                            '237322D303335352D346338612D393530302D306535343433373435646531001642564C'
                                            '716A557339463465596A5676446676346B566B')
    },
    'connack_01': {
        'desc': 'ConnACK message',
        'octstring': tc.octstring2bytearray('20020000')
    },
    'publish_01': {
        'desc': 'Publish message with QoS 1',
        'octstring': tc.octstring2bytearray('3241003A65636C697073652F696F742F74657374776172652F34626234313563382D32'
                                            '6335622D343861662D396130652D3436633334663736373266372FC406A5A5A5')
    },
    'puback_01': {
        'desc': 'PUBACK message acknowledging packet with ID 9204',
        'octstring': tc.octstring2bytearray('400223F4')
    },
    'pubrec_01': {
        'desc': 'PUBREC message acknowledging reception of packet with ID 1',
        'octstring': tc.octstring2bytearray('5F020001')
    },
    'pubrel_01': {
        'desc': 'PUBREL message acknowledging release of packet with ID 1',
        'octstring': tc.octstring2bytearray('62020001')
    },
    'pubcomp_01': {
        'desc': 'PUBCOMP message acknowledging completion of QoS 2 transfer for packet with ID 62687',
        'octstring': tc.octstring2bytearray('7002F4DF')
    },
    'subscribe_01': {
        'desc': 'Subscribe with QoS 2',
        'octstring': tc.octstring2bytearray('823FA901003A65636C697073652F696F742F74657374776172652F3462623431356338'
                                            '2D326335622D343861662D396130652D3436633334663736373266372F02')
    },
    'subscribe_02': {
        'desc': 'QoS 0 subscription with packet ID 28168 (containing ZERO WIDTH NO-BREAK SPACE U+FEFF in topic)',
        'octstring': tc.octstring2bytearray('82426E08003D65636C697073652F696F742F74657374776172652F3462623431356338'
                                            '2D326335622D343861662D396130652D3436633334663736373266372FEFBBBF00')
    },
    'suback_01': {
        'desc': 'Acknowledgment for subscription with packet ID 28168',
        'octstring': tc.octstring2bytearray('90036E0800')
    },
    'unsubscribe_01': {
        'desc': 'UNSUBSCRIBE with packet ID 0',
        'octstring': tc.octstring2bytearray('A2420000003E65636C697073652F696F742F74657374776172652F3462623431356338'
                                            '2D326335622D343861662D396130652D3436633334663736373266372F64617461')
    },
    'unsubscribe_02': {
        'desc': 'UNSUBSCRIBE with packet ID 0 and multiple topics',
        'octstring': tc.octstring2bytearray('A2420000003E65636C697073652F696F742F74657374776172652F34626234313563382D'
                                            '326335622D343861662D396130652D3436633334663736373266372F64617461003E6563'
                                            '6C697073652F696F742F74657374776172652F34626234313563382D326335622D343861'
                                            '662D396130652D3436633334663736373266372F64617461')
    },
    'unsuback_01': {
        'desc': 'Acknowledgment for un-subscription with packet ID 0',
        'octstring': tc.octstring2bytearray('B0020000')
    },
    'ping_01': {
        'desc': 'PINGREQ',
        'octstring': tc.octstring2bytearray('C000')
    },
    'ping_02': {
        'desc': 'PINGRESP',
        'octstring': tc.octstring2bytearray('D000')
    },
    'disconnect_01': {
        'desc': 'Disconnect message',
        'octstring': tc.octstring2bytearray('E000')
    }
}

coap_samples = {
    'empty_conf_01': {
        'desc': 'empty CONFirmable message version 1',
        'octstring': tc.octstring2bytearray('40003039')
    },
    'empty_conf_02': {
        'desc': 'empty CONFirmable message version 3',
        'octstring': tc.octstring2bytearray('C0003039')
    },
    'conf_01': {
        'desc': 'CONFirmable message version 1 code 0.0',
        'octstring': tc.octstring2bytearray('49003039')
    },
    'conf_02': {
        'desc': 'CONFirmable message version 1 code 0.1',
        'octstring': tc.octstring2bytearray('40013039BD0253696D706C655F5265736F75726365')
    },
    'empty_rst': {
        'desc': 'empty RESET message',
        'octstring': tc.octstring2bytearray('70003039')
    }
}
