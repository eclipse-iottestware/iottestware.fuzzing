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
from enum import Enum

from src.proto.protocol_message import AbstractMessage
from src.fuzzer.operators import UnaryOperation, BinaryOperation
from src.fuzzer.generator import AbstractGenerator


class MutatorType(Enum):
    UNARY_OP = 0,
    BINARY_OP = 1


class AbstractMutator(ABC):

    _identifier = None
    _type = None
    _field = None
    _generator = None

    def __init__(self, identifier, mutator_type):
        self._identifier = identifier
        self._type = mutator_type

    @property
    def identifier(self):
        return self._identifier

    @property
    def type(self):
        return self._type

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value: str):
        self._field = value

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, value: AbstractGenerator):
        self._generator = value

    @abstractmethod
    def compile(self):
        """
        Check the mutator and prepare/optimize if required
        # Note: method not used/required so far
        """
        pass

    @abstractmethod
    def mutate(self, message):
        pass


class BinaryOperationMutator(AbstractMutator):
    """
    Logical Mutator: AND, OR, XOR
    """

    def __init__(self, identifier, operation_type: BinaryOperation):
        super().__init__(identifier, MutatorType.BINARY_OP)
        self._operation_type = operation_type

    @property
    def operation_type(self):
        return self._operation_type

    def __str__(self):
        return 'BINARY(id={}, field={}, op={}, gen=({}))'\
            .format(self._identifier, self._field, self._operation_type, self._generator)

    def compile(self):
        pass

    def mutate(self, message: AbstractMessage):
        field_value = message.message_get_field(self.field)

        if field_value is not None:
            if self.operation_type is BinaryOperation.BINARY_XOR:
                mutated_value = BinaryOperation.xor(field_value, self.generator)
            elif self.operation_type is BinaryOperation.BINARY_OR:
                mutated_value = BinaryOperation.or_op(field_value, self.generator)
            elif self.operation_type is BinaryOperation.BINARY_AND:
                mutated_value = BinaryOperation.and_op(field_value, self.generator)
            elif self.operation_type is BinaryOperation.BINARY_SET:
                mutated_value = BinaryOperation.set_op(field_value, self.generator)
            else:
                raise Exception('BinaryMutator does not support operation {}'.format(self.operation_type))

            message.message_set_field(self.field, mutated_value)

            return '{}({})={}->{}'.format(self._operation_type, self.field, field_value, mutated_value)
        else:
            # TODO: how to handle such cases properly?
            raise Exception('Message {} has no field "{}"'.format(message.message, self.field))


class UnaryOperationMutator(AbstractMutator):
    """
    A simple UNARY_OP (e.g., NOT, INC, DEC) mutator does the actual work of altering the message
    """
    def __init__(self, identifier, operation_type: UnaryOperation):
        super().__init__(identifier, MutatorType.UNARY_OP)
        self._operation_type = operation_type

    @property
    def operation_type(self):
        return self._operation_type

    def __str__(self):
        return 'UNARY(id={}, field={}, op={})'.format(self.identifier, self.field, self.operation_type)

    def compile(self):
        pass

    def mutate(self, message: AbstractMessage):
        field_value = message.message_get_field(self.field)

        if field_value is not None:
            if self.operation_type is UnaryOperation.UNARY_INVERT:
                mutated_value = UnaryOperation.invert(field_value)
            elif self.operation_type is UnaryOperation.UNARY_INCR:
                mutated_value = UnaryOperation.increment(field_value)
            elif self.operation_type is UnaryOperation.UNARY_DECR:
                mutated_value = UnaryOperation.decrement(field_value)
            else:
                raise Exception('UnaryMutator does not support operation {}'.format(self.operation_type))

            message.message_set_field(self.field, mutated_value)

            return '{}({})={}->{}'.format(self._operation_type, self.field, field_value, mutated_value)
        else:
            # TODO: how to handle such cases properly?
            raise Exception('Message {} has no field "{}"'.format(message.message, self.field))
