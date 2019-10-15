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
from enum import Enum, auto

from src.proto.protocol_message import AbstractMessage

comparison_operators = {
    '-eq': '==',
    '-ne': '!=',
    '-gt': '>',
    '-lt': '<',
    '-ge': '>=',
    '-le': '<='
}


class FilterDirection(Enum):
    REQUEST = auto(),
    RESPONSE = auto(),
    ALL = auto()

    def __str__(self):
        if self is FilterDirection.REQUEST:
            return 'Request'
        elif self is FilterDirection.RESPONSE:
            return 'Response'
        else:
            return 'All'


class AbstractFilter(ABC):

    _identifier = None
    _description = None
    _direction = FilterDirection.ALL

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def filter_direction(self):
        return self._direction

    @filter_direction.setter
    def filter_direction(self, direction):
        self._direction = direction

    @abstractmethod
    def match(self, message):
        pass


class ComplexFilter(AbstractFilter):

    _left = None
    _right = None
    _operator = None

    def __init__(self, left: AbstractFilter, right: AbstractFilter, operator):
        self._left = left
        self._right = right
        self._operator = operator

    def __str__(self):
        return '({} {} {})'.format(self._left, self._operator, self._right)

    def match(self, message):
        if self._operator == 'AND':
            return self.__match_and(message)
        elif self._operator == 'OR':
            return self.__match_or(message)
        else:
            raise NotImplementedError('Matching Operator {}'.format(self._operator))

    def __match_and(self, message):
        left_match = self._left.match(message)
        if left_match:
            right_match = self._right.match(message)
            return left_match and right_match
        else:
            return left_match

    def __match_or(self, message):
        left_match = self._left.match(message)
        right_match = self._right.match(message)
        return left_match or right_match


class SimpleFilter(AbstractFilter):

    _field = None
    _operator = None
    _value = None
    _value_type = None

    def __str__(self):
        return '({} {} {})'.format(self.field, comparison_operators[self.operator], self.value)

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def match(self, message: AbstractMessage):
        left_operand = message.message_get_field(self.field)

        if left_operand is None:
            ret = False
        elif self.operator == '==' or comparison_operators[self.operator] == '==':
            ret = left_operand == self.value
        elif self.operator == '!=' or comparison_operators[self.operator] == '!=':
            ret = left_operand != self.value
        elif self.operator == '>' or comparison_operators[self.operator] == '>':
            ret = left_operand > self.value
        elif self.operator == '<' or comparison_operators[self.operator] == '<':
            ret = left_operand < self.value
        elif self.operator == '>=' or comparison_operators[self.operator] == '>=':
            ret = left_operand >= self.value
        elif self.operator == '<=' or comparison_operators[self.operator] == '<=':
            ret = left_operand <= self.value
        else:
            ret = False

        return ret
