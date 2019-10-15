import unittest
import src.utils.type_conversion as tc

valid_octstrings = [
    '', '00', 'FF', 'ff', 'aF', 'Be', 'AFFE', '0123456789AbCdEf', "'0123456789AbCdEf'O"
]

valid_bytearrays = [
    b'', b'\x00', b'\xff', b'\xff', b'\xaf', b'\xbe', b'\xaf\xfe', b'\x01\x23\x45\x67\x89\xab\xcd\xef',
    b'\x01\x23\x45\x67\x89\xab\xcd\xef'
]

valid_bytearray_strings = [
    '', '\\x00', '\\xff', '\\xff', '\\xaf', '\\xbe', '\\xaf\\xfe', '\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef',
    '\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef'
]

invalid_octstring = [
    '0', '-1', '123', '0123456789ABCDEF0', '0123456789ABCDEFG', 'GG', 'gg', 'ghijkl', "'00'H"
]


class TestTypeConverter(unittest.TestCase):

    def test_check_octstring_01(self):
        for vo in valid_octstrings:
            self.assertTrue(tc.check_octstring(vo), 'input {} must validate to True'.format(vo))

        for io in invalid_octstring:
            self.assertFalse(tc.check_octstring(io), 'input {} must validate to False'.format(io))

    def test_octstring2bytearray_01(self):
        zipped = zip(valid_octstrings, valid_bytearrays)
        for oct_str, exp in zipped:
            ba = tc.octstring2bytearray(oct_str)
            self.assertEqual(ba, exp, 'octstring2bytearray({}): ret={} / exp={}'.format(oct_str, ba, exp))
            self.assertIsInstance(ba, bytearray, 'Expected bytearray but got {}'.format(type(ba)))

        for io in invalid_octstring:
            with self.assertRaises(tc.ConversionException):
                tc.octstring2bytearray(io)

    def test_octstring2bytestring_01(self):
        zipped = zip(valid_octstrings, valid_bytearray_strings)
        for oct_str, exp in zipped:
            bas = tc.octstring2bytestring(oct_str)
            self.assertEqual(bas, exp, 'octstring2bytestring({}): ret={} / exp={}'.format(oct_str, bas, exp))

        for io in invalid_octstring:
            with self.assertRaises(tc.ConversionException):
                tc.octstring2bytestring(io)

    def test_bytearray2octstring_01(self):
        zipped = zip(valid_bytearrays, valid_octstrings)
        for ba, exp in zipped:
            os = tc.bytearray2octstring(ba)
            # make sure exp ends always with an O and contains only upper cases
            exp = ("'" + exp.rstrip('O').strip("'") + "'O").upper()
            self.assertEqual(os, exp, 'bytearray2octstring({}): ret={} / exp={}'.format(ba, os, exp))

    def test_bytestring2octstring_01(self):
        zipped = zip(valid_bytearray_strings, valid_octstrings)
        for bs, exp in zipped:
            os = tc.bytestring2octstring(bs)
            # make sure exp ends always with an O and contains only upper cases
            exp = ("'" + exp.rstrip('O').strip("'") + "'O").upper()
            self.assertEqual(os, exp, 'bytestring2octstring({}): ret={} / exp={}'.format(bs, os, exp))

    def test_bytestring2bytearray_01(self):
        for bs in valid_bytearray_strings:
            ba = tc.bytestring2bytearray(bs)
            self.assertIsInstance(ba, bytearray, 'Expected bytearray but got {}'.format(type(ba)))
