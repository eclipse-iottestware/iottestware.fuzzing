import unittest

from src.fuzzer.generator import RandomGenerator, FixedGenerator, \
    merge_symbol_sets, \
    ASCII_LETTERS, \
    ASCII_LOWERCASE, \
    ASCII_UPPERCASE, \
    NUMBERS, \
    PRINTABLE_SPECIAL_SYMBOLS


class TestGenerator(unittest.TestCase):

    SEED = 1
    ID = 'test_generator'

    def test_random_string_ascii_01(self):
        """test that 'random_string_ascii' produces strings of correct length and only with the given symbol sets"""
        generator = RandomGenerator(self.ID, self.SEED)
        list_of_sets = [ASCII_LETTERS, ASCII_LOWERCASE, ASCII_UPPERCASE, NUMBERS, PRINTABLE_SPECIAL_SYMBOLS]

        for symbol_set in list_of_sets:
            length = len(symbol_set)
            rnd_str = generator.random_string_ascii(symbol_set, length)
            self.assertEqual(len(rnd_str), length)      # is the length correct?
            self._validate_string(symbol_set, rnd_str)  # does the string contain only chars from set?

    def test_random_string_ascii_02(self):
        """test that 'merge_symbol_sets' merges correctly"""
        list_of_sets = [ASCII_LETTERS, ASCII_LOWERCASE, ASCII_UPPERCASE, NUMBERS, PRINTABLE_SPECIAL_SYMBOLS]
        symbol_set = merge_symbol_sets(ASCII_LETTERS, ASCII_LOWERCASE, ASCII_UPPERCASE,
                                       NUMBERS, PRINTABLE_SPECIAL_SYMBOLS)

        exp_len = 0
        for l in list_of_sets:
            exp_len += len(l)

        self.assertEqual(len(symbol_set), exp_len, 'Lengths of given lists and merged list differ')

    def _validate_string(self, symbol_set, rnd_str):
        for c in list(rnd_str):
            self.assertTrue(True if c in symbol_set else False, 'Char {} is not contained in set {}'
                            .format(c, symbol_set))

    def test_fixed_string_ascii_01(self):
        generator = FixedGenerator('0x54657354')

        for l in range(1, 21):
            rnd_str = generator.random_string_ascii(length=l)
            self.assertEqual(len(rnd_str), l, "Message length is not correct")

    def test_fixed_integers_01(self):
        generator = FixedGenerator('0x54657354')

        # Note: works only for big-endian
        rnd_uint8 = generator.random_uint8()
        self.assertEqual(rnd_uint8, 84)  # 0x54 = 84

        rnd_uint16 = generator.random_uint16()
        self.assertEqual(rnd_uint16, 21605)  # 0x5465

        rnd_uint32 = generator.random_uint32()
        self.assertEqual(rnd_uint32, 1415934804)  # 0x54657354

        rnd_uint64 = generator.random_uint64()
        self.assertEqual(rnd_uint64, 6081393677864104788)  # 0x5465735454657354
