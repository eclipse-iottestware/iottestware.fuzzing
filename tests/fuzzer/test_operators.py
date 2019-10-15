import unittest

from src.fuzzer.operators import UnaryOperation


class TestOperators(unittest.TestCase):

    def test_unary_invert_integers(self):
        values = range(1, 10)
        expected = range(-1, -10, -1)

        # input=0 as special case
        input = 0
        result = UnaryOperation.invert(input)
        expect = 1
        self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

        for idx, input in enumerate(values):
            result = UnaryOperation.invert(input)
            expect = expected[idx]
            self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_invert_floats(self):
        multiplier = 0.1
        values = range(1, 10)
        expected = range(-1, -10, -1)

        # input=0 as special case
        input = 0.0
        result = UnaryOperation.invert(input)
        expect = 1.0
        self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

        for idx, input in enumerate(values):
            result = UnaryOperation.invert(float(input) * multiplier)
            expect = float(expected[idx]) * multiplier
            self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_invert_chars(self):
        values = list('abcdefghij')
        expected = list('ABCDEFGHIJ')

        for idx, c in enumerate(values):
            result = UnaryOperation.invert(c)
            expect = expected[idx]
            self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_invert_strings(self):
        value = 'HeLlO_wOrLd'
        expect = 'hElLo_WoRlD'
        result = UnaryOperation.invert(value)
        self.assertEqual(result, expect, 'INVERT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_invert_bytes(self):
        value = b'\xFF\x00\x55\xAA'
        expected = b'\x00\xFF\xAA\x55'

        result = UnaryOperation.invert(value)
        self.assertEqual(result, expected)

    def test_unary_increment_integers(self):
        values = range(-5, 5)

        for v in values:
            expect = v + 1
            result = UnaryOperation.increment(v)
            self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_increment_floats(self):
        values = range(-5, 5)

        for v in values:
            expect = v + 1.0
            result = UnaryOperation.increment(v)
            self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_increment_strings_01(self):
        input = 'abc'
        expect = 'bcd'

        result = UnaryOperation.increment(input)
        self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_increment_strings_02(self):
        # test non-printable and special characters
        input = ''.join(chr(c) for c in range(0, 31))
        expect = ''.join(chr(c + 1) for c in range(0, 31))

        result = UnaryOperation.increment(input)
        self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_increment_strings_03(self):
        # test at large ranges with a flip to smallest char
        input = ''.join(chr(c) for c in range(1114100, 1114112))
        expect = ''.join(chr(c + 1) for c in range(1114100, 1114111)) + chr(0)

        result = UnaryOperation.increment(input)
        self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_increment_bytes(self):
        value = b'\xFF\x00\x55\xAA'
        expect = b'\x00\x01\x56\xAB'

        result = UnaryOperation.increment(value)
        self.assertEqual(result, expect, 'DECREMENT({}) = {} != expected {}'.format(value, result, expect))

    def test_unary_decrement_strings_01(self):
        input = 'bcd'
        expect = 'abc'

        result = UnaryOperation.decrement(input)
        self.assertEqual(result, expect, 'DECREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_decrement_strings_02(self):
        # test the flip to max char 0x10FFFF
        input = ''.join(chr(c) for c in range(0, 31))
        expect = chr(0x10FFFF) + ''.join(chr(c - 1) for c in range(1, 31))

        result = UnaryOperation.decrement(input)
        self.assertEqual(result, expect, 'INCREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_decrement_strings_03(self):
        # test at large ranges
        input = ''.join(chr(c) for c in range(200, 300))
        expect = ''.join(chr(c - 1) for c in range(200, 300))

        result = UnaryOperation.decrement(input)
        self.assertEqual(result, expect, 'DECREMENT({}) = {} != expected {}'.format(input, result, expect))

    def test_unary_decrement_bytes(self):
        value = b'\xFF\x00\x55\xAA'
        expect = b'\xFE\xFF\x54\xA9'

        result = UnaryOperation.decrement(value)
        self.assertEqual(result, expect, 'DECREMENT({}) = {} != expected {}'.format(value, result, expect))
