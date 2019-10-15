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

import string
from random import Random
from abc import ABC, abstractmethod

from datetime import datetime


def merge_symbol_sets(*args: str):
    ret = ''

    for a in args:
        ret += a

    return ret


# default symbol sets for string generator
ASCII_LOWERCASE = string.ascii_lowercase
ASCII_UPPERCASE = string.ascii_uppercase
ASCII_LETTERS = string.ascii_letters
NUMBERS = '0123456789'
PRINTABLE_SPECIAL_SYMBOLS = '!"#$%&\'()*+,-_./:;<>=?@[]{}\\|~'
ALL_SYMBOL_SETS = merge_symbol_sets(ASCII_LETTERS, NUMBERS, PRINTABLE_SPECIAL_SYMBOLS)

BYTE_ORDER = 'big'  # alt: 'little' TODO: configurable


class AbstractGenerator(ABC):

    @abstractmethod
    def random_bytes(self, length: int):
        """
        generate an array of random bytes with length
        :param length:
        :return:
        """
        pass

    @abstractmethod
    def random_string_ascii(self, symbol_set=ASCII_LETTERS, length: int = 10):
        pass

    @abstractmethod
    def random_uint8(self):
        """
        generates a random unsigned integer with 8 bits width
        :return: a random integer N such that 0 <= N <= 255
        """
        pass

    @abstractmethod
    def random_uint16(self):
        """
        generates a random unsigned integer with 16 bits width
        :return: a random integer N such that 0 <= N <= 65536
        """
        pass

    @abstractmethod
    def random_uint32(self):
        """
        generates a random unsigned integer with 32 bits width
        :return: a random integer N such that 0 <= N <= 2^32
        """
        pass

    @abstractmethod
    def random_uint64(self):
        """
        generates a random unsigned integer with 32 bits width
        :return: a random integer N such that 0 <= N <= 2^64
        """
        pass


class FixedGenerator(AbstractGenerator):
    """
    This class implements an AbstractGenerator but does provide only predefined fixed values
    Note: can be used e.g., as a fixed/predefined mask for the XOR mutator
    TODO: implement __init__ with a list of predefined values
    TODO: let the fixed generator implement the interface of RandomGenerator and create specific types from \
    given fixed value
    """

    def __init__(self, fixed_value: str):
        self._fixed_value_str = fixed_value
        self._fixed_value = bytes.fromhex(fixed_value.replace('0x', ''))

    def __str__(self):
        return 'fixed={}'.format(self._fixed_value_str)

    def __as_bytes_array(self, length):
        fv_len = len(self._fixed_value)
        if length < fv_len:
            rnd_str = self._fixed_value[0:length]
        else:
            mul = int(length / fv_len)
            rmd = length % fv_len
            rnd_str = self._fixed_value * mul + self._fixed_value[0:rmd]

        return rnd_str

    def random_bytes(self, length: int):
        return self.__as_bytes_array(length)

    def random_string_ascii(self, symbol_set=ASCII_LETTERS, length: int = 10):
        bytes_str = self.__as_bytes_array(length)

        ascii_str = ''
        for b in bytes_str:
            ascii_str += chr(b % 128)  # modulo to get valid ascii

        return ascii_str

    def random_uint8(self):
        bytes_str = self.__as_bytes_array(1)
        return int(bytes_str[0])

    def random_uint16(self):
        bytes_str = self.__as_bytes_array(2)
        return int.from_bytes(bytes_str, byteorder=BYTE_ORDER)

    def random_uint32(self):
        bytes_str = self.__as_bytes_array(4)
        return int.from_bytes(bytes_str, byteorder=BYTE_ORDER)

    def random_uint64(self):
        bytes_str = self.__as_bytes_array(8)
        return int.from_bytes(bytes_str, byteorder=BYTE_ORDER)


class RandomGenerator(ABC):

    def __init__(self, identifier=None, seed=None):
        self._rnd = Random()
        if seed is None:
            self._seed = int(datetime.timestamp(datetime.now()) * 1000000)
        else:
            self._seed = seed
        self._rnd.seed(seed)
        self._id = identifier if identifier is not None else self.random_string_ascii()

    def __str__(self):
        return 'id={}, seed={}'.format(self._id, self._seed)

    def reset_prng(self, seed=None):
        """
        reset the pseudo random number generator
        :param seed:
        """
        self._rnd.seed(seed)

    def random_bytes(self, length: int):
        rnd_bytes = []
        for i in range(length):
            rnd_bytes.append(self.random_uint8())

        return bytes(rnd_bytes)

    def random_string_ascii(self, symbol_set=ASCII_LETTERS, length: int = 10):
        return ''.join(self._rnd.choice(symbol_set) for i in range(length))

    def random_int(self, a, b):
        """
        simply wraps random.randint:
        :returns: an random integer N such that  a <= N <= b
        """
        return self._rnd.randint(a, b)

    def random_uint8(self):
        """
        generates a random unsigned integer with 8 bits width
        :return: a random integer N such that 0 <= N < 255
        """
        return self._rnd.randint(0, 2**8 - 1)

    def random_uint16(self):
        """
        generates a random unsigned integer with 16 bits width
        :return: a random integer N such that 0 <= N < 65536
        """
        return self._rnd.randint(0, 2**16 - 1)

    def random_uint16_bytes(self):
        """
        generates a random unsigned integer splited into two separate uint8
        :return: tuple (msb, lsb) such that 0 <= msb <= 255 and 0 <= lsb <= 255
        """
        msb = self.random_uint8()
        lsb = self.random_uint8()
        return msb, lsb

    def random_uint32(self):
        """
        generates a random unsigned integer with 32 bits width
        :return: a random integer N such that 0 <= N < 2^32
        """
        return self._rnd.randint(0, 2**32 - 1)

    def random_uint32_bytes(self):
        """
        generates a random unsigned integer splited into four separate uint8
        :return: tuple (msb_0, msb_1, lsb_0, lsb_1)
        """
        msb_0, msb_1 = self.random_uint16_bytes()
        lsb_0, lsb_1 = self.random_uint16_bytes()
        return msb_0, msb_1, lsb_0, lsb_1

    def random_uint64(self):
        """
        generates a random unsigned integer with 32 bits width
        :return: a random integer N such that 0 <= N < 2^64
        """
        return self._rnd.randint(0, 2**64 - 1)

    def random_uint64_bytes(self):
        """
        generates a random unsigned integer splited into eight separate uint8
        :return: tuple (msb_0, msb_1, msb_2, msb_3, lsb_0, lsb_1, lsb_2, lsb_3)
        """
        msb_0, msb_1, msb_2, msb_3 = self.random_uint32_bytes()
        lsb_0, lsb_1, lsb_2, lsb_3 = self.random_uint32_bytes()
        return msb_0, msb_1, msb_2, msb_3, lsb_0, lsb_1, lsb_2, lsb_3
