#!./venv/bin/python3.7
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
import argparse
from src.utils.argparse_actions import MainHelpAction, MainShortHelpAction
from src.logger import set_logging_level
from logging import INFO, DEBUG, WARNING, ERROR
from src.proto.protocol_description import ProtocolType
from src.apps.check_conf import validate_configuration
from src.apps.decode_message import decode_message
from src.apps.sample_messages import sample_messages
from src.apps.monitor import ssh_monitor
from src.apps.type_converter import convert, example_bytestring, example_octstring
from src.apps.log_processor import logstats
from src.apps.proxy_fuzzer import proxy_fuzzer

PROJECT_NAME = 'iottestware.fuzzing'
EXE_NAME = 'monkey'
VERSION = '0.0.1'
DESCRIPTION = 'The "{}" is a flexible and configurable Proxy-Fuzzer for IoT protocols like {}' \
    .format(PROJECT_NAME, ', '.join(ProtocolType.supported_protocols(False)))

# top-level parser
parser = argparse.ArgumentParser(prog=EXE_NAME, description=DESCRIPTION, add_help=False)
parser.add_argument('-v', '--version', action='version', help='Show program\'s version number and exit',
                    version='{} v{}'.format(PROJECT_NAME, VERSION))
parser.add_argument('--help', action=MainHelpAction, help='Show a long version of the help')
parser.add_argument('-h', action=MainShortHelpAction, help='Show a short version of the help')
subparsers = parser.add_subparsers(help='sub-commands')

# PARENT PARSERS
# parent parser for the (-o | -b) switch to choose between octetstring and bytestrings
oct_bytes_switch = argparse.ArgumentParser(add_help=False)
oct_bytes_switch.add_argument('input', metavar='Hex-String', help='The input string either as bytesstring '
                                                                  'or octetstring which will be converted')
oct_bytes_switch_group = oct_bytes_switch.add_mutually_exclusive_group(required=True)
oct_bytes_switch_group.add_argument('-o', action='store_true',
                                    help='Input is a TTCN-3 like octetstring e.g. {}'.format(example_octstring))
oct_bytes_switch_group.add_argument('-b', action='store_true',
                                    help='Input is a Python like bytestring e.g. {}'.format(example_bytestring))

# parent parser for protocol choice to choose between the supported protocols
protocol_switch = argparse.ArgumentParser(add_help=False)
protocol_switch.add_argument('proto', choices=ProtocolType.supported_protocols(),
                             help='Choose one of the supported protocols')

# parent parser for the logging level
log_lever_parser = argparse.ArgumentParser(add_help=False)
log_lever_parser.add_argument('--log_level', choices=['info', 'debug', 'warning', 'error'], default='error')

# COMMAND PARSERS
# create the parser for the "fuzzing" command
fuzzing_args = subparsers.add_parser('fuzzing', parents=[log_lever_parser],
                                     help='Start the Fuzzing Proxy with a given configuration')
fuzzing_args.set_defaults(func=proxy_fuzzer)
fuzzing_args.add_argument('-l', metavar='LOCAL PORT', dest='local_port',
                          required=True,
                          type=int,
                          help='Local port to listen on for requests')
fuzzing_args.add_argument('-r', metavar='HOST', dest='remote_host',
                          required=True,
                          help='Remote host which should be proxied')
fuzzing_args.add_argument('-p', metavar='REMOTE PORT', dest='remote_port',
                          required=False,
                          type=int,
                          help='Remote port which should be proxied')
fuzzing_args.add_argument('config', metavar='CONFIG',
                          help='Fuzzing Engine configuration file')
fuzzing_args.add_argument('--user', metavar='USERNAME', dest='user',
                          required=False,
                          help='Remote username on the SUT')
fuzzing_args.add_argument('--pid', metavar='PID', dest='pid',
                          required=False,
                          nargs='+',
                          type=int,
                          help='The PIDs of the process(es) which should be monitored')

# create a parser for the "validate" command
validate_args = subparsers.add_parser('validate', parents=[],
                                      help='Validate a configuration file')
validate_args.set_defaults(func=validate_configuration)
validate_args.add_argument('config', help='Fuzzing Engine configuration file')
validate_args.add_argument('-s', action='store_true', default=False,
                           help="Check only syntax and skip deeper checks")

# create a parser for the "decode" command
decode_args = subparsers.add_parser('decode', parents=[protocol_switch, oct_bytes_switch],
                                    help='Decode a single message and show summary')
decode_args.set_defaults(func=decode_message)
decode_args.add_argument('--pdfdump', action='store_true', required=False,
                         help='Generates Overview as a PDF instead of printing to stdout')

# create a parser for the "convert" command
type_convert_args = subparsers.add_parser('convert', parents=[oct_bytes_switch],
                                          help='Helper for conversion of TTCN-3 like '
                                               'octetstrings to Python\'s bytesstring '
                                               'and vice versa')
type_convert_args.set_defaults(func=convert)

# create a parser for the "protocols" command
protocols_args = subparsers.add_parser('protocols', help='Show the supported protocols')
protocols_args.set_defaults(func=lambda x: print('Supported Protocols: {}'
                                                 .format(', '.join(ProtocolType.supported_protocols(False)))))

# create a parser for the "samples" command
samples_args = subparsers.add_parser('samples', parents=[protocol_switch],
                                     help='Prints predefined samples decoded with Scapy codec')
samples_args.set_defaults(func=sample_messages)
samples_args.add_argument('-ls', action='store_true', default=False, help='Shows detailed list of field values')
samples_args.add_argument('-hex', action='store_true', default=False, help='Prints a Hex-dump of the sample')
samples_args.add_argument('-octets', action='store_true', default=False,
                          help="Show TTCN-3 like octetstring representation e.g. {}".format(example_octstring))
samples_args.add_argument('-bytes', action='store_true', default=False,
                          help='Show Python like bytearray representation e.g. {}'.format(example_bytestring))

# create a parser for the "monitor" command
monitoring_args = subparsers.add_parser('monitor', parents=[log_lever_parser],
                                        help='Monitoring of remote processes on the SUT over SSH',
                                        epilog='Note: No passwords will asked or handled here. '
                                               'Correctly configured SSH with public and private keys is expected!')
monitoring_args.set_defaults(func=ssh_monitor)
monitoring_args.add_argument('-r', metavar='HOST', required=True, help='Remote host which should be monitored')
monitoring_args.add_argument('-u', metavar='USER', required=True, help='Remote username on the SUT')
monitoring_args.add_argument('-p', metavar='PID', nargs='+', type=int, required=True,
                             help='The PID of the process which should be monitored')

# create a parser for the "logstats" command
logstats_args = subparsers.add_parser('logstats', parents=[],
                                      help='Create statistics from log files')
logstats_args.set_defaults(func=logstats)
logstats_args.add_argument('directory', help='Directory of the log files')
logstats_args.add_argument('--show', default=False, action='store_true', help='Show the plot directly')
logstats_args.add_argument('--save', default=False, action='store_true', help='Save the plot as file')

if __name__ == '__main__':
    args = parser.parse_args()
    if hasattr(args, 'func'):
        # not all commands change the logging level...
        if hasattr(args, 'log_level'):
            # set the logging level provided from CLI
            # which can be only one of 'info', 'debug', 'warning', 'error'
            if args.log_level == 'info':
                set_logging_level(INFO)
            elif args.log_level == 'debug':
                set_logging_level(DEBUG)
            elif args.log_level == 'warning':
                set_logging_level(WARNING)
            else:
                set_logging_level(ERROR)

        args.func(args)
    else:
        parser.print_usage()
