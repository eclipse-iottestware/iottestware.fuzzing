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
import src.utils.header_helper as ph

DOCS_URL = 'https://iottestware.readthedocs.io/en/master/fuzzing.html'
DOCS_MSG = '\nFor further information "Read the Docs"\n\t{}'.format(DOCS_URL)


class MainHelpAction(argparse._HelpAction):
    """
    MainHelpAction is used by --help argument in the top-level parser to display not only the basic
    help, but also all helps of all commands
    """
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                ph.print_subcommand_header(choice)
                print(subparser.format_help())

        print(DOCS_MSG)
        parser.exit()


class MainShortHelpAction(argparse._HelpAction):
    """
    MainShortHelpAction is used by -h argument in the top-level parser to display only a basic help
    """
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        print(DOCS_MSG)
        parser.exit()
