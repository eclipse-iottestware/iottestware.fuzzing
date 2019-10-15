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

# This modules contains some helper functions to ease the printing of headers, footer, separators
# on STDOUT
HORIZONTAL_CHAR = '*'
VERTICAL_CHAR = '*'

VERTICAL_SEPARATOR = '|'
HORIZONTAL_SEPARATOR = '-'


# concrete headers
# TODO: generic, print_multiline_header
def print_configuration_header(proto):
    fuzzer_info = 'Fuzzer: {}'.format(proto)
    header = 'Fuzzing Proxy Configuration'

    # calc header paddings left and right
    diff = len(fuzzer_info) - len(header) - 2
    padding_left = int(diff / 2)
    padding_right = padding_left if (diff % 2) == 0 else padding_left + 1

    print_header_line_top(len(fuzzer_info))
    print('{}{}{}{}{}'.format(VERTICAL_CHAR, ' '*padding_left, header, ' '*padding_right, VERTICAL_CHAR))
    print_header_line_bottom(len(fuzzer_info))
    print(fuzzer_info)

    return len(fuzzer_info)


def print_proxy_header(transport_type, proto_type, local, remote):
    """
    Generates a header which is shown on start-up of the fuzzing proxy.
    This header contains brief summary about the proxy configuration.
    :param transport_type: which IPL4 transport type is used e.g. TCP or UDP
    :param proto_type: which protocol is used above IPL4 e.g. MQTT or CoAP
    :param local: the local interface on which the proxy will listen for requests
    :param remote: the remote system which is proxied
    :return: summary string
    """
    lh, lp = local
    rh, rp = remote
    text_capture = 'Start Proxy {}/{}: {}:{} <-> {}:{}'.format(proto_type, transport_type, lh, lp, rh, rp)
    print_header(text_capture)


def print_proxy_footer(transport_type, proto_type, local, remote, runtime, log_dir):
    """
    Generates a footer which is shown after Ctrl+C
    :param remote: is a namedtuple address for the remote
    :param runtime: how long was the fuzzing proxy running
    :param log_dir: is the relative directory to the logs
    """
    lh, lp = local
    rh, rp = remote
    capture = 'Stop Proxy {}/{}: {}:{} <-> {}:{}'.format(proto_type, transport_type, lh, lp, rh, rp)
    runtime_capture = 'Runtime: {}'.format(runtime)
    log_dir_capture = 'Log directory: {}'.format(log_dir)

    # adjust the footer length
    footer_len = len(capture)
    if footer_len < len(runtime_capture) or footer_len < len(log_dir_capture):
        if len(runtime_capture) >= len(log_dir_capture):
            footer_len = len(runtime_capture)
        else:
            footer_len = len(log_dir_capture)
    footer_len += 4  # add for leading and closing chars

    # calculate the diff to place the close "#" at the right place
    rt_diff_len = footer_len - len(runtime_capture) - 3  # sub the leading "# " and the closing "#"
    log_diff_len = footer_len - len(log_dir_capture) - 3
    capture_diff_len = footer_len - len(capture) - 3

    print_header_line_top(footer_len)
    print('{} {}{}{}'.format(VERTICAL_CHAR, capture, ' '*capture_diff_len, VERTICAL_CHAR))
    print('{} {}{}{}'.format(VERTICAL_CHAR, runtime_capture, ' '*rt_diff_len, VERTICAL_CHAR))
    print('{} {}{}{}'.format(VERTICAL_CHAR, log_dir_capture, ' '*log_diff_len, VERTICAL_CHAR))
    print_header_line_bottom(footer_len)


def print_subcommand_header(sub_command):
    text = 'Command "{}":'.format(sub_command)
    print_horizontal_separator(80)
    print(text)


# Generic header functions
def print_header(header_caption):
    header_len = len(header_caption) + 4
    print_header_line_top(header_len)
    print('{} {} {}'.format(VERTICAL_CHAR, header_caption, VERTICAL_CHAR))
    print_header_line_bottom(header_len)


def print_header_line(length):
    print('{}'.format(HORIZONTAL_CHAR*length))


def print_header_line_top(length):
    print('\n{}'.format(HORIZONTAL_CHAR*length))


def print_header_line_bottom(length):
    print('{}\n'.format(HORIZONTAL_CHAR*length))


def print_horizontal_separator(length):
    print('{}'.format(HORIZONTAL_SEPARATOR*length))


def print_footer(footer_caption=None):
    """
    Print a line of given length with the highlight character.
    Useful is several parts need to be visually separated on the STDOUT
    :param footer_caption: the text inside the footer
    :return:
    """
    if footer_caption is None:
        # simply print a horizontal header line for now
        print_header_line_bottom(80)
    else:
        footer_len = len(footer_caption) + 4
        print_header_line_top(footer_len)
        print('{} {} {}'.format(VERTICAL_CHAR, footer_caption, VERTICAL_CHAR))
        print_header_line_bottom(footer_len)


def indent(num):
    """
    Creates a num of tabs which can be later on used to insert into prints
    Note: the value/counter of indention must managed by the using modules
    :param num:
    :return:
    """
    return '\t'*num
