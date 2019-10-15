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

from abc import ABC, abstractmethod
from src.fuzzer.filter import AbstractFilter
from src.fuzzer.distribution import AbstractUrn
from src.logger import get_default_logger
from src.fuzzer.filter import FilterDirection


class RulesEngine(object):

    def __init__(self, rules_list):
        self._complete_rule_list = rules_list
        self._all_rules = list()
        self._request_rules = list()
        self._response_rules = list()
        self._logger = get_default_logger()

        for r in rules_list:
            if r.direction == FilterDirection.ALL:
                self._request_rules.append(r)
                self._response_rules.append(r)
                self._all_rules.append(r)
            elif r.direction == FilterDirection.REQUEST:
                self._request_rules.append(r)
            elif r.direction == FilterDirection.RESPONSE:
                self._response_rules.append(r)
            else:
                raise Exception('Filter direction {} is unknown'.format(r.direction))

    def __str__(self):
        return 'Rules Enginge: {} Rules'.format(len(self.rules_list))

    def get_rules_list(self, direction: FilterDirection = FilterDirection.ALL):
        if direction == FilterDirection.ALL:
            return self._all_rules
        elif direction == FilterDirection.REQUEST:
            return self._request_rules
        elif direction == FilterDirection.RESPONSE:
            return self._response_rules
        else:
            raise Exception('Filter direction {} is unknown'.format(direction))

    @property
    def rules_list(self):
        return self._complete_rule_list

    def match(self, message, direction: FilterDirection = FilterDirection.ALL):
        """
        return all rules which match this message
        :param message: the message which should be tested against rules
        :param direction: which direction does the message take and how to match this one
        :return: list of matching rules
        """

        """ list comprehension should be faster """
        # TODO: verify
        # return [r for r in self.rules_list if r.match(message)]

        """ naive implementation """
        ret = list()
        rules = self.get_rules_list(direction)
        for r in rules:
            if r.match(message):
                self._logger.info('{} -> matched Message {}'.format(r, message.identifier))
                ret.append(r)
        return ret


class AbstractRule(ABC):

    def __init__(self, idx, identifier, match_filter: AbstractFilter):
        self._idx = idx
        self._identifier = identifier
        self._filter = match_filter
        self._logger = get_default_logger()

    @property
    def logger(self):
        return self._logger

    @property
    @abstractmethod
    def mutators(self):
        pass

    @property
    def idx(self):
        return self._idx

    @property
    def identifier(self):
        return self._identifier

    @property
    @abstractmethod
    def rule_type(self):
        pass

    @property
    def filter(self):
        return self._filter

    @property
    def direction(self):
        return self._filter.filter_direction

    def match(self, message):
        return self._filter.match(message)

    @abstractmethod
    def apply_mutator(self, message):
        pass


class Rule(AbstractRule):

    def __init__(self, idx, identifier, match_filter: AbstractFilter, mutators):
        super().__init__(idx, identifier, match_filter)
        self._mutators = mutators

    def __str__(self):
        return '{} idx={}: match({})'.format(self.rule_type, self.idx, self.filter)

    @property
    def rule_type(self):
        return 'Simple Rule'

    @property
    def mutators(self):
        return self._mutators

    def apply_mutator(self, message):
        operations = []
        for m in self._mutators:
            self.logger.info('apply {}'.format(m))
            op = m.mutate(message)
            if op:
                operations.append(op)

        return operations


class FuzzyRule(AbstractRule):
    """
    This rules has several lists of mutators and a distribution
    Each time apply_mutator() is called, the rule chooses randomly from the list of mutators and applies to the message
    :param mutators: mutators must be a 2 dimensional array, len(mutators) must fit the distribution
    """
    def __init__(self, idx, identifier, match_filter: AbstractFilter, mutators, distribution: AbstractUrn):
        super().__init__(idx, identifier, match_filter)
        self._mutators = mutators
        self._distribution = distribution
        self._next_match_idx = self.distribution.choose_element()   # required for logging

        # check if sizes fit -> should be already checked within the builder
        if len(mutators) != distribution.num_elements:
            raise Exception('Fuzzy Rule dimensions do not fit: len(mutators) != distribution.num_elements')

    def __str__(self):
        return 'FuzzyRule idx={}.{}: match({})'.format(self.idx, self._next_match_idx, self.filter)

    @property
    def distribution(self):
        return self._distribution

    @property
    def rule_type(self):
        return 'Fuzzy Rule'

    @property
    def identifier(self):
        # Note: identifier must be called before apply_mutator to get the right idx!
        return '{}.{}'.format(super().identifier, self._next_match_idx)

    @property
    def mutators(self):
        return self._mutators

    def apply_mutator(self, message):
        mutators = self.mutators[self._next_match_idx]
        operations = []

        # first use the index and then take the next -> __str__ requires the idx for logging
        self._next_match_idx = self.distribution.choose_element()

        for m in mutators:
            self.logger.info('apply {}'.format(m))
            op = m.mutate(message)
            if op:
                operations.append(op)

        return operations
