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
import re

# reg_hex = re.compile('[a-fA-F0-9]+')
__reg_oct = re.compile('^([a-fA-F0-9]{2})*$')


class ConversionException(Exception):
    pass


def strip_octstring(octstring):
    """
    remove trailing O and single quotation marks if existent
    TTCN-3 like octetstrings usually look like '1234'O
    :param octstring:
    :return:
    """
    return octstring.rstrip('O').strip("'")


def check_octstring(octstring):
    """
    Octetstrings are required to be dividable by 2 and contain only valid hex-characters
    :param octstring:
    :return:
    """
    if octstring is None:
        return False

    octstring = strip_octstring(octstring)

    # check with regular expression for valid characters
    m = __reg_oct.match(octstring)
    return bool(m)


def octstring2bytearray(octstring):
    """
    Converts a TTCN-3 like octetstring into a Python bytearray
    :param octstring:
    :return: converted bytearray
    """
    if not check_octstring(octstring):
        raise ConversionException('octetstring is invalid: {}'.format(octstring))

    octstring = strip_octstring(octstring)
    output = bytearray.fromhex(octstring)

    return output


def octstring2bytestring(octstring):
    """
    Similar to octstring2bytearray but returns a string representation of the bytearray
    :param octstring:
    :return: converted bytearray as a string
    """
    ba = octstring2bytearray(octstring)
    output = ''
    for b in ba:
        output += '\\x%02x' % b
    return output


def bytearray2octstring(byte_array):
    """
    Convert a native Python bytearray into a TTCN-3 style octetstring
    :param bytes_array:
    :return: string representing the bytearray as TTCN-3 octetstring
    """
    output = "'"
    for b in byte_array:
        output += '{:02X}'.format(b)

    output += "'O"
    return output


def bytearray2bytestring(byte_array):
    """
    Convert a native Python bytearray into a string representation
    :param byte_array:
    :return:
    """
    bs = str(byte_array).lstrip('bytearray(').rstrip(')')
    return bs


def bytestring2octstring(bytestring):
    """
    Convert a bytearray represented as a string (coming e.g. from CLI) into a octetstring
    :param bytes_string:
    :return:
    """
    bytes_string = bytestring.lstrip('b')
    octetstring = "'"

    index = 0

    while index < len(bytes_string):
        c = bytes_string[index]

        if c == '\\':
            # if a byte is encoded as something like \x00
            c_1 = bytes_string[index + 2]   # skip x and get first number
            c_2 = bytes_string[index + 3]
            octetstring += '{}{}'.format(c_1, c_2)
            index += 4
        else:
            # if a byte is encoded as a single character
            e = str(hex(ord(c))).lstrip('0x')
            octetstring += e
            index += 1

    return octetstring.upper() + "'O"


def bytestring2bytearray(bytestring):
    """
    Convert a bytearray represented as a string (coming e.g. from CLI) into a native bytearray object
    :param bytestring:
    :return:
    """
    # first translate into an octetstring
    os = bytestring2octstring(bytestring)

    # afterwards translate the octetstring into a native bytearray
    ba = octstring2bytearray(os)

    return ba
