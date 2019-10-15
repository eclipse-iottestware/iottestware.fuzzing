import unittest

from src.factory.matching_filter_builder import MatchingFilterBuilder, IncompleteFilterException
from src.fuzzer.filter import SimpleFilter, ComplexFilter
from src.proto.protocol_message import ScapyMessage, ProtocolDescription
from src.proto.protocol_description import ProtocolType

from scapy.contrib.mqtt import MQTT

# TODO: take these packets from samples
DEC_MQTT_CONNECT = b'\x10\x23\x00\x04\x4D\x51\x54\x54\x04\x02\x00\x3C\x00\x17\x6D\x6F\x73\x71\x70\x75\x62\x7C\x31' \
                   b'\x35\x30\x31\x35\x2D\x61\x6C\x65\x78\x61\x6E\x64\x65\x72'
DEC_MQTT_CONNACK = b'\x20\x00\x00\x00\x00\x00\x00'

# PUBLISH Packets with different QoS levels
DEC_MQTT_PUB_QOS0 = b'\x30\x22\x00\x13\x74\x65\x73\x74\x77\x61\x72\x65\x2F\x70\x75\x62\x6C\x69\x73\x68\x2F\x30\x32' \
                    b'\x00\x01\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'
DEC_MQTT_PUB_QOS1 = b'\x32\x22\x00\x13\x74\x65\x73\x74\x77\x61\x72\x65\x2F\x70\x75\x62\x6C\x69\x73\x68\x2F\x30\x32' \
                    b'\x00\x01\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'
DEC_MQTT_PUB_QOS2 = b'\x34\x22\x00\x13\x74\x65\x73\x74\x77\x61\x72\x65\x2F\x70\x75\x62\x6C\x69\x73\x68\x2F\x30\x32' \
                    b'\x00\x01\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'

# PUBLISH Packets with different payloads and QoS levels
# JSON1: { "name": "value" }
# JSON2:
DEC_MQTT_PUB_0_JSON1 = b'\x30\x2c\x00\x14\x68\x6f\x6d\x65\x2f\x67\x61\x72\x64\x65\x6e\x2f\x66\x6f\x75\x6e\x74\x61\x69' \
                       b'\x6e\x00\x01\x7b\x0a\x20\x22\x6e\x61\x6d\x65\x22\x3a\x20\x22\x76\x61\x6c\x75\x65\x22\x0a\x7d'
DEC_MQTT_PUB_1_JSON1 = b'\x32\x2c\x00\x14\x68\x6f\x6d\x65\x2f\x67\x61\x72\x64\x65\x6e\x2f\x66\x6f\x75\x6e\x74\x61\x69' \
                       b'\x6e\x00\x01\x7b\x0a\x20\x22\x6e\x61\x6d\x65\x22\x3a\x20\x22\x76\x61\x6c\x75\x65\x22\x0a\x7d'
DEC_MQTT_PUB_2_JSON1 = b'\x34\x2c\x00\x14\x68\x6f\x6d\x65\x2f\x67\x61\x72\x64\x65\x6e\x2f\x66\x6f\x75\x6e\x74\x61\x69' \
                       b'\x6e\x00\x01\x7b\x0a\x20\x22\x6e\x61\x6d\x65\x22\x3a\x20\x22\x76\x61\x6c\x75\x65\x22\x0a\x7d'

# SUBSCRIBE Packets
DEC_MQTT_SUB_QOS0 = b'\x82\x3F\xEE\xB0\x00\x3B\x65\x63\x6C\x69\x70\x73\x65\x2F\x69\x6F\x74\x2F\x74\x65\x73\x74\x77' \
                    b'\x61\x72\x65\x2F\x34\x62\x62\x34\x31\x35\x63\x38\x2D\x32\x63\x35\x62\x2D\x34\x38\x61\x66\x2D' \
                    b'\x39\x61\x30\x65\x2D\x34\x36\x63\x33\x34\x66\x37\x36\x37\x32\x66\x35\x2F\x00'

DEC_MQTT_DISCONNECT = b'\xe0\x00'

MQTT_PROTO_DESCRIPTION = ProtocolDescription(ProtocolType.MQTT)


class TestFilter(unittest.TestCase):

    def test_filter_builder_01(self):
        b = MatchingFilterBuilder()

        with self.assertRaises(IncompleteFilterException):
            b.build()

        b.value = 1
        with self.assertRaises(IncompleteFilterException):
            b.build()

        b.operator = '-eq'
        with self.assertRaises(IncompleteFilterException):
            b.build()

        b.identifier = 'test_filter'
        b.field = 'type'
        packet_filter = b.build()
        self.assertTrue(isinstance(packet_filter, SimpleFilter), 'FilterBuilder does not return a Filter')

    def test_simple_filter_mqtt_01(self):
        """
        Test the -eq and -ne operators
        """
        b = MatchingFilterBuilder()
        b.identifier = 'test_filter_01'
        b.value = 1
        b.field = 'type'
        b.operator = '-eq'
        con_filter = b.build()

        b.operator = '-ne'
        non_con_filter = b.build()

        b.operator = '-eq'
        b.value = 3
        publish_filter = b.build()

        b.field = 'QOS'
        b.value = 0
        qos0_filter = b.build()

        b.value = 2
        qos2_filter = b.build()

        mqtt_connect = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_CONNECT))
        mqtt_connack = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_CONNACK))
        mqtt_publish = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_PUB_QOS2))

        # match CONNECT filter
        self.assertTrue(con_filter.match(mqtt_connect))
        self.assertFalse(con_filter.match(mqtt_connack))
        self.assertFalse(con_filter.match(mqtt_publish))

        # match NON CONNECT filter
        self.assertFalse(non_con_filter.match(mqtt_connect))
        self.assertTrue(non_con_filter.match(mqtt_connack))
        self.assertTrue(non_con_filter.match(mqtt_publish))

        # match PUBLISH filter
        self.assertTrue(publish_filter.match(mqtt_publish))
        self.assertFalse(publish_filter.match(mqtt_connect))
        self.assertFalse(publish_filter.match(mqtt_connack))

        # match QoS 0 filter
        self.assertFalse(qos0_filter.match(mqtt_publish))
        # -> matches because scapy's connack packet has QoS = 0 as default
        self.assertTrue(qos0_filter.match(mqtt_connack))
        # -> matches because scapy's connect packet has QoS = 0 as default
        self.assertTrue(qos0_filter.match(mqtt_connect))

        # match QoS 2 filter
        self.assertTrue(qos2_filter.match(mqtt_publish))
        self.assertFalse(qos2_filter.match(mqtt_connack))
        self.assertFalse(qos2_filter.match(mqtt_connect))

    def test_composite_filter_mqtt_01(self):
        """
        test a composite filter
        """
        left = MatchingFilterBuilder()
        left.identifier = 'test_filter_01'
        left.value = 3
        left.field = 'type'
        left.operator = '-eq'
        pub_filter = left.build()

        right = MatchingFilterBuilder()
        right.identifier = 'test_filter_02'
        right.value = 2
        right.field = "QOS"
        right.operator = '-eq'
        qos_filter = right.build()

        comp_filter = ComplexFilter(pub_filter, qos_filter, 'AND')

        mqtt_pub_qos2 = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_PUB_QOS2))

        self.assertTrue(comp_filter.match(mqtt_pub_qos2))

    def test_composite_filter_mqtt_02(self):
        """
        test a composite filter with a more complex filter
        """
        left = MatchingFilterBuilder()
        left.identifier = 'test_filter_01'
        left.value = 3
        left.field = 'type'
        left.operator = '-eq'
        pub_filter = left.build()

        right = MatchingFilterBuilder()
        right.identifier = 'test_filter_02'
        right.value = 2
        right.field = "QOS"
        right.operator = '-lt'
        qos_filter = right.build()

        pub_qos_lt2 = ComplexFilter(pub_filter, qos_filter, 'AND')

        right = MatchingFilterBuilder()
        right.identifier = 'test_filter_03'
        right.field = 'type'
        right.value = 8
        right.operator = '-eq'
        sub_filter = right.build()

        comp_filter = ComplexFilter(pub_qos_lt2, sub_filter, 'OR')

        mqtt_pub_qos1 = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_PUB_QOS1))
        mqtt_pub_qos2 = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_PUB_QOS2))
        mqtt_sub_qos0 = ScapyMessage(MQTT_PROTO_DESCRIPTION, MQTT(DEC_MQTT_SUB_QOS0))

        # first check the simple filter
        self.assertFalse(qos_filter.match(mqtt_pub_qos2))
        self.assertTrue(qos_filter.match(mqtt_pub_qos1))
        self.assertTrue(qos_filter.match(mqtt_sub_qos0))

        self.assertTrue(sub_filter.match(mqtt_sub_qos0))
        self.assertFalse(sub_filter.match(mqtt_pub_qos1))
        self.assertFalse(sub_filter.match(mqtt_pub_qos2))

        self.assertFalse(pub_filter.match(mqtt_sub_qos0))
        self.assertTrue(pub_filter.match(mqtt_pub_qos1))
        self.assertTrue(pub_filter.match(mqtt_pub_qos2))

        # now check to composite filters
        self.assertTrue(pub_qos_lt2.match(mqtt_pub_qos1))
        self.assertFalse(pub_qos_lt2.match(mqtt_pub_qos2))
        self.assertFalse(pub_qos_lt2.match(mqtt_sub_qos0))

        self.assertFalse(comp_filter.match(mqtt_pub_qos2))
        self.assertTrue(comp_filter.match(mqtt_pub_qos1))
        self.assertTrue(comp_filter.match(mqtt_sub_qos0))
