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

from enum import Enum

from src.fuzzer.generator import AbstractGenerator


# TODO: handling not supported types in a generic manner with struct
# https://docs.python.org/3.7/library/struct.html#byte-order-size-and-alignment
# convert to bytes with struct, apply native operation and convert back original type
# import struct

class UnaryOperation(Enum):
    UNARY_INVERT = 0,
    UNARY_INCR = 1,
    UNARY_DECR = 2,

    def __str__(self):
        if self is UnaryOperation.UNARY_INVERT:
            return 'NOT'
        elif self is UnaryOperation.UNARY_INCR:
            return 'INCREMENT'
        elif self is UnaryOperation.UNARY_DECR:
            return 'DECREMENT'
        else:
            return 'UNKNOWN'

    @classmethod
    def from_string(cls, value: str):
        value = value.upper()   # avoids errors with mixing lower + upper and crashes if value is None
        if value == 'NOT':
            return UnaryOperation.UNARY_INVERT
        elif value == 'INCR':
            return UnaryOperation.UNARY_INCR
        elif value == 'DECR':
            return UnaryOperation.UNARY_DECR
        else:
            raise Exception('UnaryOperation {} not implemented'.format(value))

    # TODO: extend for signed and unsigned numeric values
    @classmethod
    def invert(cls, value):
        """
        smart invert method which can invert values depending on their type.
        :param value:
        :return:
        """
        # TODO: how to deal with inverting single flags?
        if isinstance(value, int):
            if value == 0:
                value = 1
            else:
                value *= -1
        elif isinstance(value, float):
            if value == 0.0:
                value = 1.0
            else:
                value *= -1.0
        elif isinstance(value, bool):
            value = not value
        elif isinstance(value, str):
            # inverts the cases of each character
            value = value.swapcase()
        elif isinstance(value, bytes):
            ret = b''
            for v in value:
                b = (~v & 0xFF)     # make a unsigned 8 Bit invert of the byte
                ret += bytes([b])
            value = ret
        else:
            raise NotImplementedError('invert does not support type {}'.format(type(value)))

        return value

    @classmethod
    def increment(cls, value):
        """
        smart increment method increments values depending on their type
        :param value:
        :return:
        """
        if isinstance(value, int):
            value += 1
        elif isinstance(value, float):
            value += 1.0
        elif isinstance(value, bool):
            value = cls.invert(value)
        elif isinstance(value, str):
            value = ''.join(chr(ord(c) + 1) if ord(c) < 0x10FFFF else chr(0) for c in value)
        elif isinstance(value, bytes):
            ret = b''
            for v in value:
                b = (v + 1) % 256
                ret += bytes([b])
            value = ret
        else:
            raise NotImplementedError('increment does not support type {}'.format(type(value)))

        return value

    @classmethod
    def decrement(cls, value):
        """
        smart decrement method decrements values depending on their type
        :param value:
        :return:
        """
        if isinstance(value, int):
            value -= 1
        elif isinstance(value, float):
            value -= 1.0
        elif isinstance(value, bool):
            value = cls.invert(value)
        elif isinstance(value, str):
            value = ''.join(chr(ord(c) - 1) if ord(c) > 0 else chr(0x10FFFF) for c in value)
        elif isinstance(value, bytes):
            ret = b''
            for v in value:
                b = (v - 1) % 256
                ret += bytes([b])
            value = ret
        else:
            raise NotImplementedError('decrement does not support type {}'.format(type(value)))

        return value


class BinaryOperation(Enum):
    BINARY_XOR = 0,
    BINARY_SET = 1,
    BINARY_AND = 2,
    BINARY_OR = 3

    def __str__(self):
        if self is BinaryOperation.BINARY_XOR:
            return 'XOR'
        elif self is BinaryOperation.BINARY_OR:
            return 'OR'
        elif self is BinaryOperation.BINARY_AND:
            return 'AND'
        elif self is BinaryOperation.BINARY_SET:
            return 'SET'
        else:
            return 'UNKNOWN'

    @classmethod
    def from_string(cls, value: str):
        value = value.upper()
        if value == 'XOR':
            return BinaryOperation.BINARY_XOR
        elif value == 'OR':
            return BinaryOperation.BINARY_OR
        elif value == 'AND':
            return BinaryOperation.BINARY_AND
        elif value == 'SET':
            return BinaryOperation.BINARY_SET
        else:
            raise Exception('BinaryOperation {} not implemented'.format(value))

    @classmethod
    def xor(cls, value, generator: AbstractGenerator):
        if isinstance(value, int):
            if 0 <= value < 2**8:
                mask = generator.random_uint8()
            elif 2**8 <= value < 2**16:
                mask = generator.random_uint16()
            elif 2**16 <= value < 2**32:
                mask = generator.random_uint32()
            else:
                mask = generator.random_uint64()
            value = value ^ mask
        elif isinstance(value, bytes):
            length = len(value)
            mask = generator.random_bytes(length)
            vr = []
            for i, v in enumerate(value):
                vr.append(v ^ mask[i])
            value = bytes(vr)
        else:
            raise NotImplementedError('xor does not support type {}'.format(type(value)))
        return value

    @classmethod
    def or_op(cls, value, generator: AbstractGenerator):
        if isinstance(value, int):
            if 0 <= value <= 2**8:
                mask = generator.random_uint8()
            elif 2**8 <= value < 2**16:
                mask = generator.random_uint16()
            elif 2**16 <= value < 2**32:
                mask = generator.random_uint32()
            else:
                mask = generator.random_uint64()
            value = value | mask
        elif isinstance(value, bytes):
            length = len(value)
            mask = generator.random_bytes(length)
            vr = []
            for i, v in enumerate(value):
                vr.append(v | mask[i])
            value = bytes(vr)
        else:
            raise NotImplementedError('or_op does not support type {}'.format(type(value)))
        return value

    @classmethod
    def and_op(cls, value, generator: AbstractGenerator):
        if isinstance(value, int):
            if 0 <= value < 2**8:
                mask = generator.random_uint8()
            elif 2**8 <= value < 2**16:
                mask = generator.random_uint16()
            elif 2**16 <= value < 2**32:
                mask = generator.random_uint32()
            else:
                mask = generator.random_uint64()
            value = value & mask
        elif isinstance(value, bytes):
            length = len(value)
            mask = generator.random_bytes(length)
            vr = []
            for i, v in enumerate(value):
                vr.append(v & mask[i])
            value = bytes(vr)
        else:
            raise NotImplementedError('and_op does not support type {}'.format(type(value)))
        return value

    @classmethod
    def set_op(cls, value, generator: AbstractGenerator):
        if isinstance(value, int):
            if 0 <= value < 2**8:
                mask = generator.random_uint8()
            elif 2**8 <= value < 2**16:
                mask = generator.random_uint16()
            elif 2**16 <= value < 2**32:
                mask = generator.random_uint32()
            else:
                mask = generator.random_uint64()
            value = mask
        elif isinstance(value, bytes):
            length = len(value)
            mask = generator.random_bytes(length)
            value = bytes(mask)
        else:
            raise NotImplementedError('set_op does not support type {}'.format(type(value)))
        return value
