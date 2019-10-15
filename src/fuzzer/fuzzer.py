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

from src.fuzzer.rulesengine import RulesEngine, Rule
from src.proto.protocol_message import AbstractMessage
from src.fuzzer.filter import FilterDirection
from src.logger import get_fuzzing_logger


# TODO: FuzzEngine still required? Why not using RulesEngine directly?
class FuzzingEngine(object):

    def __init__(self, rules_engine: RulesEngine):
        self._rules_engine = rules_engine
        self._logger = get_fuzzing_logger()

    @property
    def rules_enginge(self):
        return self._rules_engine

    def __str__(self):
        return 'Fuzzing Enginge:'

    def fuzz_request(self, message: AbstractMessage):
        return self.__fuzz(message, FilterDirection.REQUEST)

    def fuzz_response(self, message: AbstractMessage):
        return self.__fuzz(message, FilterDirection.RESPONSE)

    def __fuzz(self, message: AbstractMessage, direction: FilterDirection):
        """
        Fuzzer checks if any given rule matches this message and applies mutators if required
        :param message:
        :return: True if mutations applied, False otherwise
        """
        mutated = False  # any mutations applied?
        matching_rules = self._rules_engine.match(message, direction)

        for r in matching_rules:
            rule: Rule = r
            rule_id = rule.identifier
            mutators = rule.apply_mutator(message)
            mutated = True

            # log the applied fuzzing operation for post processing
            if len(mutators) > 0:
                self._logger.fuzzing_operation(rule_id, '[{}]'.format('; '.join(str(m) for m in mutators)))

        return mutated
