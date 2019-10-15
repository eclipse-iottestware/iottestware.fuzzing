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
import src.factory as build_factory
import src.utils.header_helper as ph  # Print Helper
from src.logger import remove_logging_dir


def print_fuzzing_engine(fuzzer):
    ph.print_configuration_header(fuzzer.codec)

    rules_engine = fuzzer.fuzzing_engine.rules_enginge
    print(rules_engine)

    # indention counter
    ic = 0

    # print Rules List
    for r in rules_engine.rules_list:
        match_filter = r.filter
        ph.print_horizontal_separator(80)
        print('{}Rule {}: {}'.format(ph.indent(ic), r.idx, r.rule_type))

        ic += 1
        print('{}Identifier: {}'.format(ph.indent(ic), match_filter.identifier))
        print('{}Filter: {} -> {}'.format(ph.indent(ic), r.direction, match_filter))
        if match_filter.description:
            print('{}Description: "{}"'.format(ph.indent(ic), match_filter.description))
        ic -= 1

        ic += 1
        print('{}Mutators: {}'.format(ph.indent(ic), len(r.mutators)))
        ic += 1
        for i, m in enumerate(r.mutators):
            if isinstance(m, list):
                # if multidim mutators from FuzzyRule
                print('{}alt {}: p({})'.format(ph.indent(ic), i, r.distribution.weights[i]))
                ic += 1
                for j, m2 in enumerate(m):
                    print('{}[{}.{}.{}]: {}'.format(ph.indent(ic), r.idx, i, j, m2))
                if len(m) == 0:
                    print('{}[{}.{}.0]: EMPTY MUTATOR'.format(ph.indent(ic), r.idx, i))

                ic -= 1
            else:
                print('{}[{}.{}]: {}'.format(ph.indent(ic), r.idx, i, m))
        ic -= 2

    ic -= 1
    ic -= 1

    ph.print_footer()


def validate_configuration(args):
    config_file = args.config
    config = build_factory.read_from_config_file(config_file)

    is_valid = build_factory.check_syntax(config)
    if is_valid:
        print('### Syntax check: PASS! ###')
    else:
        print('### Syntax check: FAIL! ###')

    if not args.s and is_valid:
        fuzzer = build_factory.build_from_config(config_file)
        print_fuzzing_engine(fuzzer)

        # Note: checking configuration builds here the complete fuzzing engine
        # which leads the logger to generate log folder and files which are empty not required
        # -> Remove these empty folder again
        remove_logging_dir()
