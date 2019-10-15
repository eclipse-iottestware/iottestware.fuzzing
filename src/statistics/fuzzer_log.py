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
import os
import re

from src.statistics.rotated_file import get_rotated_files
from src.logger import filename_fuzzing, get_default_logger

hb_regex = re.compile(r'(?=)(([0-9]{2}:){2}[0-9]{2}.[0-9]{3}(?<=)\s)(\[.*\]):\s(\[.*\])')


class FuzzingLog:

    def __init__(self, log_dir):
        self._log_dir = log_dir
        self._rules = dict()
        self._logger = get_default_logger()

    @property
    def rule_ids(self):
        return self._rules.keys()

    @property
    def num_rules(self):
        return len(self._rules)

    # TODO: these are not timestamps but rather strings with the time!
    def get_rule_appearances(self, rule_id):
        if rule_id in self._rules:
            return self._rules[rule_id].get('timestamps')
        else:
            return []

    def parse(self):
        fuzz_ops_filename = os.path.join(self._log_dir, filename_fuzzing)
        if not os.path.isfile(fuzz_ops_filename) or not os.path.exists(fuzz_ops_filename):
            self._logger.error('{} does not exist or is not a file'.format(fuzz_ops_filename))
            return False

        files = get_rotated_files(fuzz_ops_filename)
        for fuzz_ops_log_file in files:
            with open(fuzz_ops_log_file) as f:
                for l in f:
                    matches = hb_regex.finditer(l)
                    for i, m in enumerate(matches):
                        log_timestamp = m.group(1).strip()  # timestamp of the logevent
                        mutator_id = m.group(3)[1:-1]  # remove [] around the name

                        # TODO: initialize via default:
                        # https://docs.quantifiedcode.com/python-anti-patterns/correctness/not_using_defaultdict.html
                        if mutator_id not in self._rules:
                            timestamps = list()
                            self._rules[mutator_id] = {'appearances': 0, 'timestamps': timestamps}

                        m = self._rules[mutator_id]
                        m['timestamps'].append(log_timestamp)
                        m['appearances'] += 1

        return True
